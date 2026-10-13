"""Funções de matemática atuarial (vida) com mortalidade de Gompertz-Makeham.

Parâmetros padrão: Standard Ultimate Survival Model (SUSM) de
Dickson, Hardy & Waters, *Actuarial Mathematics for Life Contingent Risks*.
    mu_x = A + B * c**x,  A = 0.00022, B = 2.7e-6, c = 1.124
"""

from __future__ import annotations

import math
from dataclasses import dataclass

IDADE_MAXIMA = 130


@dataclass(frozen=True)
class Makeham:
    A: float = 0.00022
    B: float = 2.7e-6
    c: float = 1.124

    def tpx(self, x: float, t: float) -> float:
        """Probabilidade de (x) sobreviver t anos."""
        if t <= 0:
            return 1.0
        ln_c = math.log(self.c)
        return math.exp(-self.A * t - self.B * self.c**x * (self.c**t - 1) / ln_c)

    def qx(self, x: float) -> float:
        """Probabilidade de (x) morrer em até 1 ano."""
        return 1.0 - self.tpx(x, 1)


SUSM = Makeham()


def v(i: float) -> float:
    """Fator de desconto anual."""
    return 1.0 / (1.0 + i)


def expectativa_vida(x: float, modelo: Makeham = SUSM) -> float:
    """Expectativa de vida completa aproximada: e_x = sum_{k>=1} kpx + 1/2."""
    return sum(modelo.tpx(x, k) for k in range(1, IDADE_MAXIMA - int(x) + 1)) + 0.5


def anuidade_antecipada(x: float, i: float, modelo: Makeham = SUSM, n: int | None = None) -> float:
    """ä_x (vitalícia) ou ä_x:n (temporária), pagamentos anuais de 1 no início do ano."""
    termos = IDADE_MAXIMA - int(x) if n is None else n
    return sum(v(i) ** k * modelo.tpx(x, k) for k in range(termos))


def anuidade_mensal(x: float, i: float, modelo: Makeham = SUSM) -> float:
    """ä_x^(12) pela aproximação de Woolhouse com dois termos: ä_x - 11/24."""
    return anuidade_antecipada(x, i, modelo) - 11 / 24


def seguro_vida_inteira(x: float, i: float, modelo: Makeham = SUSM) -> float:
    """A_x = 1 - d * ä_x (capital 1 pago no fim do ano da morte)."""
    d = i / (1 + i)
    return 1.0 - d * anuidade_antecipada(x, i, modelo)


def premio_nivelado(x: float, i: float, capital: float, modelo: Makeham = SUSM) -> float:
    """Prêmio anual nivelado (vitalício) para um seguro de vida inteira: S * A_x / ä_x."""
    return capital * seguro_vida_inteira(x, i, modelo) / anuidade_antecipada(x, i, modelo)


def plano_aposentadoria(
    idade_atual: int,
    idade_aposentadoria: int,
    renda_mensal: float,
    taxa_anual: float,
    saldo_inicial: float = 0.0,
    modelo: Makeham = SUSM,
) -> dict:
    """Reserva necessária para uma renda vitalícia e o aporte mensal que a constitui.

    Na acumulação os aportes são certos (sem mortalidade), capitalizados à taxa mensal
    equivalente. Na aposentadoria, a renda é vitalícia: reserva = 12 * renda * ä_x^(12).
    """
    if idade_aposentadoria <= idade_atual:
        raise ValueError("A idade de aposentadoria deve ser maior que a idade atual.")

    i_m = (1 + taxa_anual) ** (1 / 12) - 1
    meses = (idade_aposentadoria - idade_atual) * 12
    reserva = 12 * renda_mensal * anuidade_mensal(idade_aposentadoria, taxa_anual, modelo)

    saldo_projetado = saldo_inicial * (1 + i_m) ** meses
    falta = max(reserva - saldo_projetado, 0.0)
    fator_acumulacao = meses if i_m == 0 else ((1 + i_m) ** meses - 1) / i_m * (1 + i_m)
    aporte = falta / fator_acumulacao

    return {
        "reserva_necessaria": reserva,
        "aporte_mensal": aporte,
        "meses_contribuicao": meses,
        "total_aportado": aporte * meses,
        "expectativa_vida_na_aposentadoria": expectativa_vida(idade_aposentadoria, modelo),
    }
