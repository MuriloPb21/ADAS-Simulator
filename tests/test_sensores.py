import pytest

from app.sensores import distancia_validada


def test_distancia_validada():
    resultado = distancia_validada(25, 27, 23)

    assert resultado == 25


def test_distancia_com_leituras_desordenadas():
    resultado = distancia_validada(40, 20, 30)

    assert resultado == 30


def test_distancia_com_valores_iguais():
    resultado = distancia_validada(50, 50, 50)

    assert resultado == 50


def test_sensor_com_leitura_negativa():
    with pytest.raises(ValueError):
        distancia_validada(25, -5, 23)
