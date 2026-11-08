from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.calculos import distancia_segura, margem_lateral
from app.sensores import distancia_validada
from app.sistema import status_frontal, status_faixa, status_geral

from app.database import Base, engine, get_db
from app.models import Simulacao


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


@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensagem": "ADAS Simulator API funcionando!",
        "status": "online"
    }


@app.post("/simular")
def simular(
    dados: DadosSimulacao,
    db: Session = Depends(get_db)
):

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

    # Salvar simulação no banco de dados
    nova_simulacao = Simulacao(
        vel_atual=dados.vel_atual,
        vel_frente=dados.vel_frente,

        radar=dados.radar,
        lidar=dados.lidar,
        camera=dados.camera,

        atrito=dados.atrito,
        nivel=dados.nivel,

        faixa_esq=dados.faixa_esq,
        faixa_dir=dados.faixa_dir,

        distancia_validada=dist_validada,
        distancia_segura=dist_segura,

        status_frontal=frontal,
        aeb_acionado=(frontal == "RISCO DE COLISAO"),

        margem_lateral=margem,

        faixa_esquerda=esquerda,
        faixa_direita=direita,

        status_geral=geral
    )

    db.add(nova_simulacao)
    db.commit()
    db.refresh(nova_simulacao)

    return {
        "distancia_validada": dist_validada,
        "distancia_segura": dist_segura,
        "status_frontal": frontal,
        "aeb": "ACIONADO" if frontal == "RISCO DE COLISAO" else "NAO ACIONADO",
        "margem_lateral": margem,
        "faixa_esquerda": esquerda,
        "faixa_direita": direita,
        "status_geral": geral,
        "id": nova_simulacao.id,
        "criado_em": nova_simulacao.criado_em.isoformat(),
    }


@app.get("/historico")
def historico(db: Session = Depends(get_db)):
    simulacoes = (
        db.query(Simulacao)
        .order_by(Simulacao.criado_em.desc())
        .all()
    )

    return [
        {
            "id": simulacao.id,
            "criado_em": simulacao.criado_em.isoformat(),

            # Dados de entrada
            "vel_atual": simulacao.vel_atual,
            "vel_frente": simulacao.vel_frente,
            "radar": simulacao.radar,
            "lidar": simulacao.lidar,
            "camera": simulacao.camera,
            "atrito": simulacao.atrito,
            "nivel": simulacao.nivel,
            "faixa_esq": simulacao.faixa_esq,
            "faixa_dir": simulacao.faixa_dir,

            # Resultados
            "distancia_validada": simulacao.distancia_validada,
            "distancia_segura": simulacao.distancia_segura,
            "margem_lateral": simulacao.margem_lateral,

            # Decisões do sistema
            "status_frontal": simulacao.status_frontal,
            "aeb_acionado": simulacao.aeb_acionado,
            "faixa_esquerda": simulacao.faixa_esquerda,
            "faixa_direita": simulacao.faixa_direita,
            "status_geral": simulacao.status_geral
        }
        for simulacao in simulacoes
    ]