from datetime import date, datetime

from bling_sdk.models import (
    BlingModel,
    Contato,
    NotaFiscal,
    PedidoVenda,
    Produto,
    Saldo,
    Tributacao,
    para_camel,
)


def test_para_camel():
    assert para_camel("descricao_curta") == "descricaoCurta"
    assert para_camel("id_produto_pai") == "idProdutoPai"
    assert para_camel("nome") == "nome"
    assert para_camel("id") == "id"
    assert para_camel("data_alteracao_inicial") == "dataAlteracaoInicial"


def test_alias_camel_na_leitura_e_na_escrita():
    p = Produto.model_validate({"descricaoCurta": "c", "idProdutoPai": 7, "precoCusto": 1.5})
    assert (p.descricao_curta, p.id_produto_pai, p.preco_custo) == ("c", 7, 1.5)
    assert p.bruto() == {"descricaoCurta": "c", "idProdutoPai": 7, "precoCusto": 1.5}


def test_snake_case_tambem_e_aceito_na_construcao():
    assert Produto(descricao_curta="c").bruto() == {"descricaoCurta": "c"}


def test_acronimos_irregulares():
    t = Tributacao.model_validate(
        {
            "nFCI": "f",
            "codigoANP": "1",
            "descricaoANP": "d",
            "percentualGLP": 2.5,
            "valorICMSSubstituto": 3.0,
        }
    )
    assert (t.n_fci, t.codigo_anp, t.descricao_anp) == ("f", "1", "d")
    assert (t.percentual_glp, t.valor_icms_substituto) == (2.5, 3.0)
    assert set(t.bruto()) == {
        "nFCI",
        "codigoANP",
        "descricaoANP",
        "percentualGLP",
        "valorICMSSubstituto",
    }


def test_imagem_url():
    p = Produto.model_validate({"imagemURL": "http://x/y.jpg"})
    assert p.imagem_url == "http://x/y.jpg"
    assert p.bruto() == {"imagemURL": "http://x/y.jpg"}


def test_campo_desconhecido_sobrevive_ao_round_trip():
    """O Bling adiciona campos continuamente (duns entrou em produtos recentemente)."""
    p = Produto.model_validate({"id": 1, "campoQueAindaNaoExiste": {"a": [1, 2]}})
    assert p.model_extra == {"campoQueAindaNaoExiste": {"a": [1, 2]}}
    assert p.bruto()["campoQueAindaNaoExiste"] == {"a": [1, 2]}


def test_modelo_vazio_nao_manda_nada():
    """Critico: `camposCustomizados: []` num PUT apagaria todos os campos customizados."""
    assert Produto().bruto() == {}
    assert PedidoVenda().bruto() == {}
    assert Contato().bruto() == {}
    assert NotaFiscal().bruto() == {}


def test_nenhum_default_de_tenant():
    """O schema antigo embutia dados de uma empresa: marca, categoria, ncm, unidade."""
    p = Produto()
    assert p.marca is None
    assert p.categoria is None
    assert p.tributacao is None
    assert p.unidade is None
    assert p.tipo is None and p.situacao is None and p.formato is None
    assert p.campos_customizados == []


def test_read_modify_write_preserva_tudo():
    p = Produto.model_validate(
        {
            "id": 1,
            "nome": "Copo",
            "marca": "Minha Marca",
            "tributacao": {"ncm": "1234.56.78"},
            "camposCustomizados": [{"idCampoCustomizado": 9, "valor": "x"}],
            "campoNovo": "preservado",
        }
    )
    p.preco = 19.9
    corpo = p.bruto()
    assert corpo["preco"] == 19.9
    assert corpo["marca"] == "Minha Marca"
    assert corpo["tributacao"] == {"ncm": "1234.56.78"}
    assert corpo["camposCustomizados"] == [{"idCampoCustomizado": 9, "valor": "x"}]
    assert corpo["campoNovo"] == "preservado"


def test_datahora_serializa_com_espaco():
    """O Bling emite e aceita "2024-09-27 11:24:56" -- o T do ISO e recusado."""
    n = NotaFiscal(data_emissao=datetime(2024, 9, 27, 11, 24, 56))
    assert n.bruto()["dataEmissao"] == "2024-09-27 11:24:56"


def test_datahora_le_o_formato_com_espaco():
    n = NotaFiscal.model_validate({"dataEmissao": "2024-09-27 11:24:56"})
    assert n.data_emissao == datetime(2024, 9, 27, 11, 24, 56)


def test_data_serializa_sem_hora():
    assert Produto(data_validade=date(2026, 12, 31)).bruto()["dataValidade"] == "2026-12-31"


def test_variacoes_aninhadas():
    p = Produto.model_validate(
        {"id": 1, "formato": "V", "variacoes": [{"id": 2, "nomeVariacao": "P"}]}
    )
    assert p.variacoes[0].id == 2
    assert p.variacoes[0].nome_variacao == "P"


def test_ref_aparece_onde_o_bling_usa_id():
    p = Produto.model_validate({"categoria": {"id": 99}, "linhaProduto": {"id": 5}})
    assert p.categoria.id == 99 and p.linha_produto.id == 5


def test_saldo_com_depositos():
    s = Saldo.model_validate(
        {
            "produto": {"id": 1},
            "saldoFisicoTotal": 10.5,
            "saldoVirtualTotal": 8.0,
            "depositos": [{"id": 3, "saldoFisico": 10.5, "saldoVirtual": 8.0}],
        }
    )
    assert s.produto.id == 1
    assert s.depositos[0].saldo_virtual == 8.0


def test_acesso_por_item():
    assert Produto(nome="x")["nome"] == "x"


def test_payload_real_da_doc_valida():
    """Exemplo de produto copiado do webhook v1 da doc oficial."""
    p = Produto.model_validate(
        {
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
    )
    assert (p.nome, p.preco, p.formato) == ("Copo do Bling", 4.99, "S")
    assert p.model_extra == {}


def test_decimal_entra_como_float():
    from decimal import Decimal

    assert Produto(preco=Decimal("9.90")).preco == 9.9


def test_blingmodel_base_aceita_qualquer_coisa():
    m = BlingModel.model_validate({"o": "que", "vier": [1]})
    assert m.model_extra == {"o": "que", "vier": [1]}
