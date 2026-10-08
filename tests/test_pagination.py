from datetime import date

import httpx
import pytest
import respx

from bling_sdk import fatiar_periodo, iter_paginas
from bling_sdk.config import INTERVALO_MAXIMO_FILTRO
from conftest import HOST


def pagina(n, qtd):
    return {"data": [{"id": n * 1000 + i} for i in range(qtd)]}


# --- iter_paginas sobre o cliente ----------------------------------------------------------


@respx.mock
def test_tres_paginas_cheia_cheia_curta(cliente):
    rota = respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(200, json=pagina(1, 100)),
            httpx.Response(200, json=pagina(2, 100)),
            httpx.Response(200, json=pagina(3, 7)),
        ]
    )
    itens = list(cliente.produtos.iter_todos(limite=100))
    assert len(itens) == 207
    assert rota.call_count == 3
    assert [c.request.url.params["pagina"] for c in rota.calls] == ["1", "2", "3"]


@respx.mock
def test_ultima_pagina_exatamente_cheia_custa_uma_request_vazia(cliente):
    """O Bling nao devolve total nem cursor: pagina curta/vazia e o unico sinal de fim."""
    rota = respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(200, json=pagina(1, 2)),
            httpx.Response(200, json={"data": []}),
        ]
    )
    assert len(list(cliente.produtos.iter_todos(limite=2))) == 2
    assert rota.call_count == 2


@respx.mock
def test_max_paginas_limita(cliente):
    rota = respx.get(f"{HOST}/produtos").respond(json=pagina(1, 10))
    assert len(list(cliente.produtos.iter_todos(limite=10, max_paginas=2))) == 20
    assert rota.call_count == 2


@respx.mock
def test_iterador_e_lazy(cliente):
    rota = respx.get(f"{HOST}/produtos").respond(json=pagina(1, 10))
    it = cliente.produtos.iter_todos(limite=10)
    assert rota.call_count == 0, "nada deve sair na rede antes do primeiro next()"
    next(it)
    assert rota.call_count == 1


@respx.mock
def test_filtros_sao_repassados_em_toda_pagina(cliente):
    rota = respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(200, json=pagina(1, 2)),
            httpx.Response(200, json=pagina(2, 1)),
        ]
    )
    list(cliente.produtos.iter_todos(limite=2, tipo="P"))
    assert all(c.request.url.params["tipo"] == "P" for c in rota.calls)


@respx.mock
def test_iter_todos_nao_aceita_pagina(cliente):
    respx.get(f"{HOST}/produtos").respond(json={"data": []})
    with pytest.raises(TypeError):
        list(cliente.produtos.iter_todos(pagina=3))


# --- iter_paginas isolado ------------------------------------------------------------------


def test_iter_paginas_para_na_pagina_curta():
    chamadas = []

    def buscar(*, pagina, limite, **kw):
        chamadas.append(pagina)
        return list(range(limite)) if pagina < 3 else [1]

    assert len(list(iter_paginas(buscar, limite=10))) == 21
    assert chamadas == [1, 2, 3]


def test_iter_paginas_primeira_pagina_vazia():
    assert list(iter_paginas(lambda **kw: [], limite=10)) == []


def test_iter_paginas_respeita_pagina_inicial():
    vistas = []

    def buscar(*, pagina, limite, **kw):
        vistas.append(pagina)
        return []

    list(iter_paginas(buscar, pagina_inicial=5))
    assert vistas == [5]


# --- fatiar_periodo ------------------------------------------------------------------------


def test_fatiar_periodo_nunca_passa_de_um_ano():
    fatias = list(fatiar_periodo(date(2020, 1, 1), date(2026, 1, 1)))
    assert len(fatias) > 1
    for inicio, fim in fatias:
        assert fim - inicio <= INTERVALO_MAXIMO_FILTRO


def test_fatias_sao_contiguas_e_cobrem_o_periodo():
    inicial, final = date(2023, 3, 15), date(2026, 7, 1)
    fatias = list(fatiar_periodo(inicial, final))
    assert fatias[0][0] == inicial
    assert fatias[-1][1] == final
    for (_, fim_a), (inicio_b, _) in zip(fatias, fatias[1:], strict=False):
        assert (inicio_b - fim_a).days == 1


def test_periodo_curto_vira_uma_fatia():
    assert list(fatiar_periodo(date(2026, 1, 1), date(2026, 2, 1))) == [
        (date(2026, 1, 1), date(2026, 2, 1))
    ]


def test_passo_customizado():
    fatias = list(fatiar_periodo(date(2026, 1, 1), date(2026, 1, 10), dias=3))
    assert fatias == [
        (date(2026, 1, 1), date(2026, 1, 4)),
        (date(2026, 1, 5), date(2026, 1, 8)),
        (date(2026, 1, 9), date(2026, 1, 10)),
    ]


def test_final_antes_de_inicial_levanta():
    with pytest.raises(ValueError, match="final"):
        list(fatiar_periodo(date(2026, 2, 1), date(2026, 1, 1)))
