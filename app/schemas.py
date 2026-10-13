from pydantic import BaseModel, Field


class LinhaTabua(BaseModel):
    idade: int
    qx: float
    lx: float
    ex: float


class AnuidadeEntrada(BaseModel):
    idade: int = Field(ge=0, le=110, examples=[60])
    taxa_juros: float = Field(gt=-0.5, lt=1, description="Taxa anual efetiva (0.05 = 5%)", examples=[0.05])


class AnuidadeSaida(BaseModel):
    anuidade_antecipada: float = Field(description="ä_x")
    anuidade_mensal: float = Field(description="ä_x^(12)")
    seguro_vida_inteira: float = Field(description="A_x")


class SeguroEntrada(BaseModel):
    idade: int = Field(ge=0, le=110, examples=[30])
    taxa_juros: float = Field(gt=-0.5, lt=1, examples=[0.05])
    capital: float = Field(gt=0, examples=[100_000])


class SeguroSaida(BaseModel):
    premio_unico: float
    premio_anual_nivelado: float


class PlanoEntrada(BaseModel):
    idade_atual: int = Field(ge=14, le=90, examples=[25])
    idade_aposentadoria: int = Field(ge=40, le=100, examples=[65])
    renda_mensal: float = Field(gt=0, examples=[5000])
    taxa_juros: float = Field(ge=0, lt=1, examples=[0.04])
    saldo_inicial: float = Field(default=0, ge=0)


class PlanoSaida(BaseModel):
    reserva_necessaria: float
    aporte_mensal: float
    meses_contribuicao: int
    total_aportado: float
    expectativa_vida_na_aposentadoria: float
