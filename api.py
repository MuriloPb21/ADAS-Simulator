from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.calculos import distancia_segura, margem_lateral
from app.sensores import distancia_validada
from app.sistema import status_frontal, status_faixa, status_geral

class DadosSimulacao(BaseModel):
    vel_atual: float = Field(ge=0)
    vel_frente: float = Field(ge=0)

    radar: float = Field(ge=0)
    lidar: float = Field(ge=0)
    camera: float = Field(ge=0)

    atrito: float = Field(gt=0)
    nivel: int = Field(ge=1, le=3)

    faixa_esq: float = Field(ge=0)
    faixa_dir: float = Field(ge=0)

app = FastAPI(
    title="ADAS Simulator API",
    description="API para simulação de sistemas avançados de assistência ao motorista.",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensagem": "ADAS Simulator API funcionando!",
        "status": "online"
    }


@app.post("/simular")
def simular(dados: DadosSimulacao):

    # Validar as leituras dos sensores
    dist_validada = distancia_validada(
        dados.radar,
        dados.lidar,
        dados.camera
    )

    # Calcular a distância segura
    dist_segura = distancia_segura(
        dados.vel_atual,
        dados.nivel,
        dados.atrito
    )

    # Verificar o risco de colisão frontal
    frontal = status_frontal(
        dados.vel_atual,
        dados.vel_frente,
        dist_validada,
        dist_segura
    )

    # Calcular a margem lateral
    margem = margem_lateral(dados.vel_atual)

    # Verificar as faixas laterais
    esquerda = status_faixa(dados.faixa_esq, margem)
    direita = status_faixa(dados.faixa_dir, margem)

    # Determinar o status geral
    geral = status_geral(frontal, esquerda, direita)

    return {
        "distancia_validada": dist_validada,
        "distancia_segura": dist_segura,
        "status_frontal": frontal,
        "aeb": "ACIONADO" if frontal == "RISCO DE COLISAO" else "NAO ACIONADO",
        "margem_lateral": margem,
        "faixa_esquerda": esquerda,
        "faixa_direita": direita,
        "status_geral": geral
    }