from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app import atuaria
from app.schemas import (
    AnuidadeEntrada,
    AnuidadeSaida,
    LinhaTabua,
    PlanoEntrada,
    PlanoSaida,
    SeguroEntrada,
    SeguroSaida,
)

app = FastAPI(
    title="Atuária API",
    description=(
        "Cálculos de matemática atuarial: tábua de vida, anuidades, seguros e planejamento de aposentadoria."
    ),
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/", tags=["status"])
def raiz() -> dict:
    return {"status": "ok", "docs": "/docs"}


@app.get("/tabua", response_model=list[LinhaTabua], tags=["mortalidade"])
def tabua(
    de: int = Query(0, ge=0, le=120),
    ate: int = Query(110, ge=0, le=120),
    raiz_lx: float = Query(100_000, gt=0, description="Radix l_0 da tábua"),
) -> list[LinhaTabua]:
    """Tábua de vida (Gompertz-Makeham / SUSM) entre as idades informadas."""
    if ate < de:
        raise HTTPException(422, "'ate' deve ser maior ou igual a 'de'.")
    m = atuaria.SUSM
    return [
        LinhaTabua(
            idade=x,
            qx=m.qx(x),
            lx=raiz_lx * m.tpx(0, x),
            ex=atuaria.expectativa_vida(x),
        )
        for x in range(de, ate + 1)
    ]


@app.post("/anuidade", response_model=AnuidadeSaida, tags=["valores presentes"])
def anuidade(entrada: AnuidadeEntrada) -> AnuidadeSaida:
    x, i = entrada.idade, entrada.taxa_juros
    return AnuidadeSaida(
        anuidade_antecipada=atuaria.anuidade_antecipada(x, i),
        anuidade_mensal=atuaria.anuidade_mensal(x, i),
        seguro_vida_inteira=atuaria.seguro_vida_inteira(x, i),
    )


@app.post("/seguro-vida", response_model=SeguroSaida, tags=["valores presentes"])
def seguro_vida(entrada: SeguroEntrada) -> SeguroSaida:
    x, i, s = entrada.idade, entrada.taxa_juros, entrada.capital
    return SeguroSaida(
        premio_unico=s * atuaria.seguro_vida_inteira(x, i),
        premio_anual_nivelado=atuaria.premio_nivelado(x, i, s),
    )


@app.post("/aposentadoria/plano", response_model=PlanoSaida, tags=["aposentadoria"])
def plano(entrada: PlanoEntrada) -> PlanoSaida:
    try:
        resultado = atuaria.plano_aposentadoria(
            entrada.idade_atual,
            entrada.idade_aposentadoria,
            entrada.renda_mensal,
            entrada.taxa_juros,
            entrada.saldo_inicial,
        )
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    return PlanoSaida(**resultado)
