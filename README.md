# 📊 Atuária API

[![CI](https://github.com/<seu-usuario>/atuaria-api/actions/workflows/ci.yml/badge.svg)](https://github.com/<seu-usuario>/atuaria-api/actions/workflows/ci.yml)

API REST em **Python + FastAPI** com cálculos de **matemática atuarial de vida**: tábua de mortalidade, anuidades, seguros e planejamento de aposentadoria.

A mortalidade segue a **lei de Gompertz-Makeham** com os parâmetros do *Standard Ultimate Survival Model* (Dickson, Hardy & Waters, *Actuarial Mathematics for Life Contingent Risks*):

$$\mu_x = A + B\,c^x,\quad A = 0{,}00022,\; B = 2{,}7\times10^{-6},\; c = 1{,}124$$

Os testes conferem os resultados contra valores publicados no livro (ä₆₀ = 14,9041 e A₆₀ = 0,29028, a 5% a.a.).

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/tabua?de=0&ate=110` | Tábua de vida: `qx`, `lx` e expectativa `ex` |
| `POST` | `/anuidade` | ä<sub>x</sub>, ä<sub>x</sub><sup>(12)</sup> e A<sub>x</sub> para uma idade e taxa |
| `POST` | `/seguro-vida` | Prêmio único e prêmio anual nivelado de um seguro de vida inteira |
| `POST` | `/aposentadoria/plano` | Reserva necessária para uma renda vitalícia e o aporte mensal que a constitui |

A documentação interativa (Swagger) fica em **`/docs`**.

### Exemplo

```bash
curl -X POST http://localhost:8000/aposentadoria/plano \
  -H "Content-Type: application/json" \
  -d '{"idade_atual": 25, "idade_aposentadoria": 65, "renda_mensal": 5000, "taxa_juros": 0.04}'
```

```json
{
  "reserva_necessaria": 864975.60,
  "aporte_mensal": 742.55,
  "meses_contribuicao": 480,
  "total_aportado": 356426.17,
  "expectativa_vida_na_aposentadoria": 22.74
}
```

## Como executar

**Localmente**

```bash
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

**Com Docker**

```bash
docker build -t atuaria-api .
docker run -p 8000:8000 atuaria-api
```

**Testes e lint**

```bash
pytest -v
ruff check . && ruff format --check .
```

## Estrutura

```
app/
├── atuaria.py   # funções atuariais puras (sem dependência de framework)
├── schemas.py   # modelos Pydantic de entrada e saída
└── main.py      # rotas FastAPI
tests/           # testes unitários e de API (pytest)
```

## Tecnologias

FastAPI · Pydantic v2 · Uvicorn · pytest · Ruff · Docker · GitHub Actions

## Licença

[MIT](LICENSE)
