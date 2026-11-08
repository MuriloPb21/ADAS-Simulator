
from .calculos import mediana


def distancia_validada(
    radar: float,
    lidar: float,
    camera: float
) -> float:
    """
    Valida as leituras dos sensores e retorna a mediana
    das três distâncias.
    """

    leituras = [radar, lidar, camera]

    for leitura in leituras:
        if leitura < 0:
            raise ValueError("As distâncias não podem ser negativas.")

    return mediana(radar, lidar, camera)