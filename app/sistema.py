
def status_frontal(
    vel_atual: float,
    vel_frente: float,
    dist_validada: float,
    dist_segura: float
) -> str:
    """Classifica o risco de colisão frontal."""

    vel_relativa = vel_atual - vel_frente

    if vel_relativa <= 0:
        return "SEGURO"

    elif dist_validada >= dist_segura:
        return "SEGURO"

    elif dist_validada >= 0.5 * dist_segura:
        return "ATENCAO"

    else:
        return "RISCO DE COLISAO"
    

def status_faixa(distancia: float, margem: float) -> str:
    """Classifica o risco de invasão das faixas laterais."""

    if distancia < margem:
        return "PERIGO DE INVASAO"
    elif distancia < margem + 0.20:
        return "ATENCAO"
    else:
        return "NORMAL"


def status_geral(
    frontal: str,
    esquerda: str,
    direita: str
) -> str:
    """Determina o estado geral do sistema ADAS."""

    if (
        frontal == "RISCO DE COLISAO"
        or esquerda == "PERIGO DE INVASAO"
        or direita == "PERIGO DE INVASAO"
    ):
        return "INTERVENCAO CRITICA EXIGIDA"

    elif (
        frontal == "ATENCAO"
        or esquerda == "ATENCAO"
        or direita == "ATENCAO"
    ):
        return "ATENCAO"

    else:
        return "NORMAL"

    vel_relativa = vel_atual - vel_frente

    if vel_relativa <= 0 or dist_validada >= dist_segura:
        return "SEGURO"

    elif dist_validada >= 0.5 * dist_segura:
        return "ATENCAO"

    else:
        return "RISCO DE COLISAO"