from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_raiz():
    assert client.get("/").json()["status"] == "ok"


def test_tabua():
    r = client.get("/tabua", params={"de": 20, "ate": 25})
    assert r.status_code == 200
    linhas = r.json()
    assert [l["idade"] for l in linhas] == list(range(20, 26))
    assert linhas[0]["lx"] > linhas[-1]["lx"]


def test_tabua_intervalo_invalido():
    assert client.get("/tabua", params={"de": 50, "ate": 40}).status_code == 422


def test_anuidade():
    r = client.post("/anuidade", json={"idade": 60, "taxa_juros": 0.05})
    assert r.status_code == 200
    assert round(r.json()["anuidade_antecipada"], 3) == 14.904


def test_seguro_vida():
    r = client.post("/seguro-vida", json={"idade": 30, "taxa_juros": 0.05, "capital": 100_000})
    corpo = r.json()
    assert r.status_code == 200
    assert 0 < corpo["premio_anual_nivelado"] < corpo["premio_unico"] < 100_000


def test_plano_aposentadoria():
    r = client.post(
        "/aposentadoria/plano",
        json={"idade_atual": 25, "idade_aposentadoria": 65, "renda_mensal": 5000, "taxa_juros": 0.04},
    )
    assert r.status_code == 200
    assert r.json()["aporte_mensal"] > 0


def test_plano_idades_invertidas():
    r = client.post(
        "/aposentadoria/plano",
        json={"idade_atual": 60, "idade_aposentadoria": 55, "renda_mensal": 5000, "taxa_juros": 0.04},
    )
    assert r.status_code == 422
