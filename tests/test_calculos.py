
import pytest

from app.calculos import (
    mediana,
    tempo_reacao,
    distancia_segura,
    margem_lateral
)


def test_mediana():
    assert mediana(25, 30, 20) == 25


def test_tempo_reacao():
    assert tempo_reacao(1) == 1.0
    assert tempo_reacao(2) == 1.5
    assert tempo_reacao(3) == 2.0


def test_tempo_reacao_invalido():
    with pytest.raises(ValueError):
        tempo_reacao(4)


def test_distancia_segura():
    resultado = distancia_segura(100, 2, 0.8)
    assert resultado == pytest.approx(90.83, abs=0.01)


def test_velocidade_negativa():
    with pytest.raises(ValueError):
        distancia_segura(-10, 2, 0.8)


def test_atrito_invalido():
    with pytest.raises(ValueError):
        distancia_segura(100, 2, 0)


def test_margem_lateral():
    assert margem_lateral(80) == 0.50
    assert margem_lateral(100) == 0.70


def test_margem_velocidade_negativa():
    with pytest.raises(ValueError):
        margem_lateral(-10)