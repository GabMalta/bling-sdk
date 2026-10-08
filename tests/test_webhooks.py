"""Os payloads abaixo sao copiados dos exemplos v1 de developer.bling.com.br/webhooks."""

import hashlib
import hmac
import json

import pytest

from bling_sdk import (
    BlingAssinaturaInvalida,
    assinar,
    exigir_assinatura,
    parse_evento,
    verificar_assinatura,
)
from bling_sdk.models.webhooks import (
    EstoqueVirtualWebhook,
    EstoqueWebhook,
    NotaFiscalWebhook,
    PayloadExcluido,
    PedidoVendaWebhook,
    ProdutoFornecedorWebhook,
    ProdutoWebhook,
)
from bling_sdk.webhooks import ACOES, RECURSOS

SEGREDO = "68eb85dcad967396d05fecdd00802117d7515264b520c362e7f46619aa09"

PRODUTO = {
    "id": 12345678,
    "nome": "Copo do Bling",
    "codigo": "COD-4587",
    "tipo": "P",
    "situacao": "A",
    "preco": 4.99,
    "unidade": "UN",
    "formato": "S",
    "idProdutoPai": 12345678,
    "categoria": {"id": 12345679},
    "descricaoCurta": "Descricao curta",
    "descricaoComplementar": "Descricao complementar",
}
PEDIDO = {
    "id": 12345678,
    "data": "2024-09-25",
    "numero": 123,
    "numeroLoja": "Loja_123",
    "total": 123.45,
    "contato": {"id": 12345678},
    "vendedor": {"id": 12345678},
    "loja": {"id": 12345678},
    "situacao": {"id": 12345678, "valor": 12345678},
}
ESTOQUE = {
    "produto": {"id": 12345678},
    "deposito": {"id": 12345678, "saldoFisico": 1250.75, "saldoVirtual": 1250.75},
    "operacao": "E",
    "quantidade": 25,
    "saldoFisicoTotal": 1500.75,
    "saldoVirtualTotal": 1500.75,
}
ESTOQUE_VIRTUAL = {
    "produto": {"id": 12345},
    "saldoFisicoTotal": 150.75,
    "saldoVirtualTotal": 148.50,
    "vinculoComplexo": True,
    "depositos": [
        {"id": 1, "saldoFisico": 75.25, "saldoVirtual": 73.00},
        {"id": 2, "saldoFisico": 75.50, "saldoVirtual": 75.50},
    ],
}
PRODUTO_FORNECEDOR = {
    "id": 12345678,
    "descricao": "Copo do Bling",
    "codigo": "COD-123",
    "precoCusto": 3.9,
    "precoCompra": 3.5,
    "padrao": False,
    "garantia": 3,
    "produto": {"id": 12345678},
    "fornecedor": {"id": 12345678},
}
NOTA = {
    "id": 12345678,
    "tipo": 1,
    "situacao": 1,
    "numero": "1234",
    "dataEmissao": "2024-09-27 11:24:56",
    "dataOperacao": "2024-09-27 11:00:00",
    "contato": {"id": 12345678},
    "naturezaOperacao": {"id": 12345678},
    "loja": {"id": 12345678},
}


def envelope(event, data):
    return {
        "eventId": "01945027-150e-72b4-e7cf-4943a042cd9c",
        "date": "2025-01-10 12:18:46",
        "version": "v1",
        "event": event,
        "companyId": "d4475854366a36c86a37e792f9634a51",
        "data": data,
    }


def corpo_bytes(event, data):
    return json.dumps(envelope(event, data)).encode()


def header(corpo, segredo=SEGREDO):
    return "sha256=" + hmac.new(segredo.encode(), corpo, hashlib.sha256).hexdigest()


# --- assinatura -----------------------------------------------------------------------------


def test_assinatura_valida():
    c = corpo_bytes("product.updated", PRODUTO)
    assert verificar_assinatura(c, header(c), SEGREDO) is True


def test_assinatura_invalida():
    c = corpo_bytes("product.updated", PRODUTO)
    assert verificar_assinatura(c, header(c, "outro-segredo"), SEGREDO) is False


def test_hex_pelado_e_aceito():
    c = corpo_bytes("product.updated", PRODUTO)
    assert verificar_assinatura(c, assinar(c, SEGREDO), SEGREDO) is True


def test_prefixo_maiusculo_e_aceito():
    c = corpo_bytes("product.updated", PRODUTO)
    assert verificar_assinatura(c, header(c).replace("sha256=", "SHA256="), SEGREDO) is True


def test_assinatura_ausente_e_invalida():
    c = corpo_bytes("product.updated", PRODUTO)
    assert verificar_assinatura(c, None, SEGREDO) is False
    assert verificar_assinatura(c, "", SEGREDO) is False


def test_verificacao_e_byte_exata():
    """Re-serializar o JSON muda ordem de chave e espacamento, logo muda o digest.

    E por isso que a API recebe `bytes` e nunca um dict.
    """
    original = corpo_bytes("product.updated", PRODUTO)
    assinatura = header(original)
    reserializado = json.dumps(json.loads(original), sort_keys=True, indent=2).encode()
    assert reserializado != original
    assert verificar_assinatura(reserializado, assinatura, SEGREDO) is False


def test_usa_compare_digest(monkeypatch):
    chamou = []
    original = hmac.compare_digest
    monkeypatch.setattr(
        hmac, "compare_digest", lambda a, b: chamou.append(True) or original(a, b)
    )
    c = corpo_bytes("product.updated", PRODUTO)
    verificar_assinatura(c, header(c), SEGREDO)
    assert chamou, "comparacao de credencial tem de ser em tempo constante"


def test_exigir_assinatura_levanta_com_mensagem_util():
    c = corpo_bytes("product.updated", PRODUTO)
    with pytest.raises(BlingAssinaturaInvalida, match="BYTES crus"):
        exigir_assinatura(c, "sha256=deadbeef", SEGREDO)


def test_parse_evento_verifica_antes_de_parsear():
    """Corpo forjado e recusado sem ser interpretado como JSON."""
    with pytest.raises(BlingAssinaturaInvalida):
        parse_evento(b"{nao e json valido", assinatura="sha256=00", client_secret=SEGREDO)


# --- envelope -------------------------------------------------------------------------------


def test_envelope():
    c = corpo_bytes("product.updated", PRODUTO)
    e = parse_evento(c, assinatura=header(c), client_secret=SEGREDO)
    assert e.event_id == "01945027-150e-72b4-e7cf-4943a042cd9c"
    assert e.version == "v1"
    assert e.recurso == "product"
    assert e.acao == "updated"
    assert e.company_id == "d4475854366a36c86a37e792f9634a51"
    assert isinstance(e.company_id, str), "companyId e um hash de 32 chars, nao um int"


def test_parse_sem_segredo_nao_verifica():
    parse_evento(corpo_bytes("product.created", PRODUTO))


# --- despacho de payload --------------------------------------------------------------------


@pytest.mark.parametrize(
    ("event", "data", "esperado"),
    [
        ("order.created", PEDIDO, PedidoVendaWebhook),
        ("order.updated", PEDIDO, PedidoVendaWebhook),
        ("product.created", PRODUTO, ProdutoWebhook),
        ("product.updated", PRODUTO, ProdutoWebhook),
        ("stock.created", ESTOQUE, EstoqueWebhook),
        ("stock.updated", ESTOQUE, EstoqueWebhook),
        ("virtual_stock.updated", ESTOQUE_VIRTUAL, EstoqueVirtualWebhook),
        ("product_supplier.created", PRODUTO_FORNECEDOR, ProdutoFornecedorWebhook),
        ("invoice.created", NOTA, NotaFiscalWebhook),
        ("consumer_invoice.updated", NOTA, NotaFiscalWebhook),
    ],
)
def test_payload_despacha_para_o_modelo_certo(event, data, esperado):
    e = parse_evento(corpo_bytes(event, data))
    assert type(e.payload()) is esperado


@pytest.mark.parametrize("recurso", sorted(RECURSOS))
def test_deleted_carrega_apenas_id(recurso):
    e = parse_evento(corpo_bytes(f"{recurso}.deleted", {"id": 12345678}))
    p = e.payload()
    assert isinstance(p, PayloadExcluido)
    assert p.id == 12345678


def test_recurso_desconhecido_nao_estoura():
    e = parse_evento(corpo_bytes("coisa_nova.updated", {"x": 1}))
    assert e.payload().model_extra == {"x": 1}


# --- campos especificos ---------------------------------------------------------------------


def test_produto_mapeia_camel_para_snake():
    p = parse_evento(corpo_bytes("product.updated", PRODUTO)).payload()
    assert p.id_produto_pai == 12345678
    assert p.descricao_curta == "Descricao curta"
    assert p.categoria.id == 12345679


def test_estoque_mapeia_saldos():
    p = parse_evento(corpo_bytes("stock.updated", ESTOQUE)).payload()
    assert p.operacao == "E"
    assert p.saldo_fisico_total == 1500.75
    assert p.deposito.saldo_virtual == 1250.75


def test_vinculo_complexo():
    """True significa >200 produtos vinculados: os saldos tem de ser relidos pela API."""
    p = parse_evento(corpo_bytes("virtual_stock.updated", ESTOQUE_VIRTUAL)).payload()
    assert p.vinculo_complexo is True
    assert [d.id for d in p.depositos] == [1, 2]


def test_nota_mapeia_datahora_com_espaco():
    p = parse_evento(corpo_bytes("invoice.created", NOTA)).payload()
    assert p.data_emissao.hour == 11 and p.data_emissao.minute == 24
    assert p.natureza_operacao.id == 12345678


def test_situacao_do_pedido_preserva_valor():
    p = parse_evento(corpo_bytes("order.updated", PEDIDO)).payload()
    assert p.situacao.model_extra == {"id": 12345678, "valor": 12345678}


def test_constantes_documentadas():
    assert ACOES == {"created", "updated", "deleted"}
    assert "virtual_stock" in RECURSOS and len(RECURSOS) == 7
