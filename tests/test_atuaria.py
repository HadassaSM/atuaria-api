import pytest

from app import atuaria


def test_valores_de_referencia_susm():
    # Dickson, Hardy & Waters — SUSM a 5%: ä_60 = 14.9041, A_60 = 0.29028
    assert atuaria.anuidade_antecipada(60, 0.05) == pytest.approx(14.9041, abs=1e-3)
    assert atuaria.seguro_vida_inteira(60, 0.05) == pytest.approx(0.29028, abs=1e-4)


def test_tpx_decresce_com_tempo_e_idade():
    m = atuaria.SUSM
    assert m.tpx(40, 0) == 1.0
    assert m.tpx(40, 10) > m.tpx(40, 20)
    assert m.qx(80) > m.qx(40)


def test_expectativa_diminui_com_idade():
    assert atuaria.expectativa_vida(30) > atuaria.expectativa_vida(60) > 0


def test_anuidade_temporaria_de_um_ano_vale_um():
    assert atuaria.anuidade_antecipada(50, 0.05, n=1) == pytest.approx(1.0)


def test_plano_com_saldo_suficiente_nao_exige_aporte():
    p = atuaria.plano_aposentadoria(30, 65, 1000, 0.04, saldo_inicial=10_000_000)
    assert p["aporte_mensal"] == 0
    assert p["meses_contribuicao"] == 35 * 12


def test_plano_aporte_acumula_a_reserva():
    p = atuaria.plano_aposentadoria(25, 65, 5000, 0.04)
    i_m = 1.04 ** (1 / 12) - 1
    saldo = 0.0
    for _ in range(p["meses_contribuicao"]):
        saldo = (saldo + p["aporte_mensal"]) * (1 + i_m)
    assert saldo == pytest.approx(p["reserva_necessaria"])


def test_plano_idades_invalidas():
    with pytest.raises(ValueError):
        atuaria.plano_aposentadoria(65, 60, 1000, 0.04)
