from app.calculos import distancia_segura, margem_lateral
from app.sensores import distancia_validada
from app.sistema import status_frontal, status_faixa, status_geral

def entradas():

    vel_atual = float(input("Velocidade do veículo atual (km/h): "))
    vel_frente = float(input("Velocidade do veículo à frente (km/h): "))
    radar = float(input("Leitura do sensor radar (metros): "))
    lidar = float(input("Leitura do sensor lidar (metros): "))
    camera = float(input("Leitura do sensor câmera (metros): "))
    atrito = float(input("Atrito da via (ex: 0.8, 0.4, 0.25): "))
    nivel = int(input("Nível de sensibilidade ADAS (1=esportivo, 2=normal, 3=seguro): "))
    faixa_esq = float(input("Distância da faixa esquerda (metros): "))
    faixa_dir = float(input("Distância da faixa direita (metros): "))

    dist_validada = distancia_validada(radar, lidar, camera)
    dist_segura = distancia_segura(vel_atual, nivel, atrito)

    frontal = status_frontal(
        vel_atual,
        vel_frente,
        dist_validada,
        dist_segura
    )

    margem = margem_lateral(vel_atual)

    esquerda = status_faixa(faixa_esq, margem)
    direita = status_faixa(faixa_dir, margem)

    geral = status_geral(frontal, esquerda, direita)

    print()

    print(f"Distância validada: {dist_validada:.2f} m")
    print(f"Distância segura: {dist_segura:.2f} m")
    print(f"Status frontal: {frontal}")

    if frontal == "RISCO DE COLISAO":
        print("AEB: ACIONADO")
    else:
        print("AEB: não acionado")

    print(f"Margem lateral exigida: {margem:.2f} m")
    print(f"Faixa esquerda: {esquerda}")
    print(f"Faixa direita: {direita}")
    print(f"STATUS GERAL: {geral}")

if __name__ == "__main__":
    entradas()