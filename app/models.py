
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime

from app.database import Base


class Simulacao(Base):
    __tablename__ = "simulacoes"

    id = Column(Integer, primary_key=True, index=True)

    criado_em = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Dados de entrada
    vel_atual = Column(Float, nullable=False)
    vel_frente = Column(Float, nullable=False)

    radar = Column(Float, nullable=False)
    lidar = Column(Float, nullable=False)
    camera = Column(Float, nullable=False)

    atrito = Column(Float, nullable=False)
    nivel = Column(Integer, nullable=False)

    faixa_esq = Column(Float, nullable=False)
    faixa_dir = Column(Float, nullable=False)

    # Resultados da simulação
    distancia_validada = Column(Float, nullable=False)
    distancia_segura = Column(Float, nullable=False)

    status_frontal = Column(String, nullable=False)
    aeb_acionado = Column(Boolean, nullable=False)

    margem_lateral = Column(Float, nullable=False)

    faixa_esquerda = Column(String, nullable=False)
    faixa_direita = Column(String, nullable=False)

    status_geral = Column(String, nullable=False)