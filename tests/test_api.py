from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200

    assert resposta.json() == {
        "mensagem": "ADAS Simulator API funcionando!",
        "status": "online"
    }


def test_simulacao():
    dados = {
        "vel_atual": 100,
        "vel_frente": 80,
        "radar": 100,
        "lidar": 102,
        "camera": 98,
        "atrito": 0.8,
        "nivel": 2,
        "faixa_esq": 0.8,
        "faixa_dir": 0.9
    }

    resposta = client.post("/simular", json=dados)

    assert resposta.status_code == 200

    resultado = resposta.json()

    assert resultado["distancia_validada"] == 100
    assert resultado["status_frontal"] == "SEGURO"
    assert resultado["aeb"] == "NAO ACIONADO"
    assert resultado["status_geral"] == "ATENCAO"


def test_simulacao_dados_invalidos():
    dados = {
        "vel_atual": -100,
        "vel_frente": 80,
        "radar": 100,
        "lidar": 102,
        "camera": 98,
        "atrito": 0.8,
        "nivel": 5,
        "faixa_esq": 0.8,
        "faixa_dir": 0.9
    }

    resposta = client.post("/simular", json=dados)

    assert resposta.status_code == 422


def test_simulacao_atrito_zero():
    dados = {
        "vel_atual": 100,
        "vel_frente": 80,
        "radar": 100,
        "lidar": 102,
        "camera": 98,
        "atrito": 0,
        "nivel": 2,
        "faixa_esq": 0.8,
        "faixa_dir": 0.9
    }

    resposta = client.post("/simular", json=dados)

    assert resposta.status_code == 422


def test_simulacao_campo_ausente():
    dados = {
        "vel_atual": 100,
        "vel_frente": 80,
        "radar": 100,
        "lidar": 102,
        "camera": 98,
        "atrito": 0.8,
        "nivel": 2,
        "faixa_esq": 0.8
    }

    resposta = client.post("/simular", json=dados)

    assert resposta.status_code == 422

def test_simulacao_sensor_negativo():
    dados = {
        "vel_atual": 100,
        "vel_frente": 80,
        "radar": -1,
        "lidar": 102,
        "camera": 98,
        "atrito": 0.8,
        "nivel": 2,
        "faixa_esq": 0.8,
        "faixa_dir": 0.9
    }

    resposta = client.post("/simular", json=dados)

    assert resposta.status_code == 422

def test_simulacao_faixa_negativa():
    dados = {
        "vel_atual": 100,
        "vel_frente": 80,
        "radar": 100,
        "lidar": 102,
        "camera": 98,
        "atrito": 0.8,
        "nivel": 2,
        "faixa_esq": 0.8,
        "faixa_dir": -0.5
    }

    resposta = client.post("/simular", json=dados)

    assert resposta.status_code == 422