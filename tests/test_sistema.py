
from app.sistema import (
    status_frontal,
    status_faixa,
    status_geral
)


# TESTES FRONTAIS

def test_status_frontal_seguro():
    resultado = status_frontal(100, 80, 100, 90)

    assert resultado == "SEGURO"


def test_status_frontal_atencao():
    resultado = status_frontal(100, 80, 60, 90)

    assert resultado == "ATENCAO"


def test_status_frontal_risco():
    resultado = status_frontal(100, 80, 30, 90)

    assert resultado == "RISCO DE COLISAO"


# TESTES DE FAIXA

def test_status_faixa_perigo():
    resultado = status_faixa(0.60, 0.70)

    assert resultado == "PERIGO DE INVASAO"


def test_status_faixa_atencao():
    resultado = status_faixa(0.80, 0.70)

    assert resultado == "ATENCAO"


def test_status_faixa_normal():
    resultado = status_faixa(1.00, 0.70)

    assert resultado == "NORMAL"


# TESTES DO STATUS GERAL

def test_status_geral_critico():
    resultado = status_geral(
        "RISCO DE COLISAO",
        "NORMAL",
        "NORMAL"
    )

    assert resultado == "INTERVENCAO CRITICA EXIGIDA"


def test_status_geral_atencao():
    resultado = status_geral(
        "SEGURO",
        "ATENCAO",
        "NORMAL"
    )

    assert resultado == "ATENCAO"


def test_status_geral_normal():
    resultado = status_geral(
        "SEGURO",
        "NORMAL",
        "NORMAL"
    )

    assert resultado == "NORMAL"
