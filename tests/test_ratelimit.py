import threading
import time

import pytest

from bling_sdk.ratelimit import (
    ArquivoRateLimiter,
    JanelaDeslizanteRateLimiter,
    SemLimite,
    limitador_padrao,
    limpar_limitadores,
    registrar_limitador,
)

# time.monotonic() no Windows tem resolucao de ~15,6 ms (GetTickCount64), e o tempo MEDIDO
# quantiza nesse passo: uma espera real de 0,203 s pode ser lida como 0,187. Toda assercao de
# tempo desconta uma tick, senao o teste falha de forma intermitente sem nada estar errado.
TICK = time.get_clock_info("monotonic").resolution


def pelo_menos(decorrido: float, esperado: float) -> None:
    assert decorrido >= esperado - TICK, f"esperado >= {esperado}, medido {decorrido:.4f}"


@pytest.fixture(autouse=True)
def _registro_limpo():
    limpar_limitadores()
    yield
    limpar_limitadores()


def test_tres_chamadas_cabem_rapido_a_quarta_espera():
    lim = JanelaDeslizanteRateLimiter(3, periodo=0.3)
    inicio = time.monotonic()
    for _ in range(3):
        lim.acquire()
    tres = time.monotonic() - inicio
    lim.acquire()
    quatro = time.monotonic() - inicio

    # O intervalo minimo espaca as tres primeiras, mas a quarta espera a janela inteira.
    assert quatro > tres
    pelo_menos(quatro, 0.3)


def test_intervalo_minimo_impede_rajada():
    """Sem intervalo minimo, as 3 chamadas sairiam no mesmo milissegundo.

    A garantia e sobre o tempo TOTAL, nao sobre o intervalo entre retornos: os slots sao
    reservados em instantes ideais, entao se um `sleep` passa do ponto o intervalo medido
    do par seguinte encolhe. O que protege a cota e o acumulado.
    """
    lim = JanelaDeslizanteRateLimiter(3, periodo=0.3, margem=0.0)
    inicio = time.monotonic()
    for _ in range(3):
        lim.acquire()
    decorrido = time.monotonic() - inicio
    # intervalo minimo = 0.3/3 = 0.1; a 1a sai na hora, a 2a em +0.1, a 3a em +0.2.
    pelo_menos(decorrido, 0.2)


def test_max_chamadas_invalido():
    with pytest.raises(ValueError, match="max_chamadas"):
        JanelaDeslizanteRateLimiter(0)


def test_penalize_pausa_todas_as_threads():
    lim = JanelaDeslizanteRateLimiter(100, periodo=0.01)
    lim.penalize(0.3)

    liberadas: list[float] = []
    inicio = time.monotonic()

    def trabalhar():
        lim.acquire()
        liberadas.append(time.monotonic() - inicio)

    threads = [threading.Thread(target=trabalhar) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(liberadas) == 4
    pelo_menos(min(liberadas), 0.3)


def test_penalize_nao_encurta_pausa_existente():
    lim = JanelaDeslizanteRateLimiter(3)
    lim.penalize(10.0)
    lim.penalize(0.01)
    inicio = time.monotonic()
    # Nao esperamos os 10s: so confirmamos que a pausa longa segue valendo.
    assert lim._pausado_ate - inicio > 5.0


def test_limitador_padrao_e_singleton_por_empresa():
    a1 = limitador_padrao("legitima")
    a2 = limitador_padrao("legitima")
    b = limitador_padrao("outra")
    assert a1 is a2, "duas instancias da mesma conta devem dividir o orcamento"
    assert a1 is not b, "contas diferentes precisam de orcamentos independentes"


def test_rate_padrao_vem_do_ambiente(monkeypatch):
    monkeypatch.setenv("BLING_SDK_RATE_LIMIT", "7")
    assert limitador_padrao("x")._max_chamadas == 7


def test_rate_invalido_cai_no_padrao(monkeypatch):
    monkeypatch.setenv("BLING_SDK_RATE_LIMIT", "abacaxi")
    assert limitador_padrao("x")._max_chamadas == 3


def test_registrar_substitui_o_limitador():
    falso = SemLimite()
    registrar_limitador("legitima", falso)
    assert limitador_padrao("legitima") is falso


def test_sem_limite_nao_bloqueia():
    lim = SemLimite()
    inicio = time.monotonic()
    for _ in range(50):
        lim.acquire()
    lim.penalize(100.0)
    lim.acquire()
    assert time.monotonic() - inicio < 0.1


# --- cross-process ------------------------------------------------------------------------


def test_arquivo_limiter_espaca_chamadas(tmp_path):
    lim = ArquivoRateLimiter(tmp_path / "rl.json", max_chamadas=2, periodo=0.2)
    inicio = time.monotonic()
    for _ in range(4):
        lim.acquire()
    pelo_menos(time.monotonic() - inicio, 0.2)


def test_dois_limiters_no_mesmo_arquivo_coordenam(tmp_path):
    """Simula dois processos: instancias separadas, estado compartilhado em disco."""
    caminho = tmp_path / "rl.json"
    a = ArquivoRateLimiter(caminho, max_chamadas=2, periodo=0.4)
    b = ArquivoRateLimiter(caminho, max_chamadas=2, periodo=0.4)

    inicio = time.monotonic()
    a.acquire()
    b.acquire()
    a.acquire()
    b.acquire()  # a 4a chamada no total precisa esperar a janela virar
    pelo_menos(time.monotonic() - inicio, 0.4)


def test_arquivo_limiter_penalize_atravessa_instancias(tmp_path):
    caminho = tmp_path / "rl.json"
    a = ArquivoRateLimiter(caminho, max_chamadas=50, periodo=0.01)
    b = ArquivoRateLimiter(caminho, max_chamadas=50, periodo=0.01)
    a.penalize(0.3)
    inicio = time.monotonic()
    b.acquire()
    pelo_menos(time.monotonic() - inicio, 0.3)


def test_arquivo_corrompido_e_resetado_nao_levanta(tmp_path):
    """Estado de rate limit e descartavel; token nao e. Tratamentos opostos de proposito."""
    caminho = tmp_path / "rl.json"
    caminho.write_text("nao e json", encoding="utf-8")
    ArquivoRateLimiter(caminho, max_chamadas=3).acquire()
