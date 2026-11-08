
def mediana(a: float, b: float, c: float) -> float:
    """Retorna o valor central entre três leituras."""

    return sorted([a, b, c])[1]


def tempo_reacao(nivel: int) -> float:
    """Retorna o tempo de reação conforme o nível de sensibilidade."""

    tempos = {
        1: 1.0,
        2: 1.5,
        3: 2.0
    }

    if nivel not in tempos:
        raise ValueError("O nível deve ser 1, 2 ou 3.")

    return tempos[nivel]


def distancia_segura(
    vel_kmh: float,
    nivel: int,
    atrito: float
) -> float:
    """Calcula a distância segura considerando reação e frenagem."""

    if vel_kmh < 0:
        raise ValueError("A velocidade não pode ser negativa.")

    if atrito <= 0:
        raise ValueError("O atrito deve ser maior que zero.")

    v = vel_kmh / 3.6

    return (
        v * tempo_reacao(nivel)
        + (v ** 2) / (2 * atrito * 9.81)
    )


def margem_lateral(vel_atual: float) -> float:
    """Calcula a margem lateral exigida conforme a velocidade."""

    if vel_atual < 0:
        raise ValueError("A velocidade não pode ser negativa.")

    if vel_atual <= 80:
        return 0.50

    return 0.50 + (vel_atual - 80) * 0.01