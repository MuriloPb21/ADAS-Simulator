# ADAS Simulator 🚗

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Pytest](https://img.shields.io/badge/Tests-28%20passed-success.svg)](https://docs.pytest.org/)

Simulador educacional de sistemas avançados de assistência ao motorista (ADAS), desenvolvido em Python.

O projeto simula funcionalidades de assistência veicular, utilizando leituras de sensores, cálculos de distância segura e identificação de possíveis riscos de colisão e invasão de faixa.

## 🎯 Objetivo

Desenvolver uma aplicação que simule o funcionamento de alguns recursos presentes em sistemas ADAS, aplicando conceitos de programação, organização de código, testes automatizados e desenvolvimento de APIs.

## ⚙️ Funcionalidades

- Validação e processamento de leituras de sensores (Radar, LiDAR e câmera).
- Cálculo de distância segura considerando velocidade, tempo de reação e atrito da via.
- Monitoramento de distância frontal e identificação de riscos de colisão.
- Monitoramento de faixas laterais.
- Classificação geral dos níveis de risco.
- Simulação de acionamento do sistema AEB.
- API REST para receber dados e retornar resultados em JSON.
- Validação automática dos dados de entrada (via Pydantic).

## 🛠️ Tecnologias utilizadas

- **Python**
- **FastAPI**
- **Pydantic**
- **Pytest**
- **Uvicorn**
- **HTTPX**

## 📁 Estrutura do projeto

```text
ADAS-Simulator/
│
├── app/
│   ├── __init__.py
│   ├── calculos.py
│   ├── sensores.py
│   └── sistema.py
│
├── tests/
│   ├── test_api.py
│   ├── test_calculos.py
│   ├── test_sensores.py
│   └── test_sistema.py
│
├── api.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/MuriloPb21/ADAS-Simulator.git
```

### 2. Acessar a pasta do projeto

```bash
cd ADAS-Simulator
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Executar a API

```bash
python -m uvicorn api:app --reload
```

### 5. Acessar a documentação

Com o servidor em execução, acesse:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

A documentação interativa permite enviar dados para a API e visualizar os resultados da simulação em tempo real.

## 🧪 Testes automatizados

O projeto possui **28 testes automatizados**, cobrindo cálculos, sensores, sistema ADAS e endpoints da API.

Para executar os testes:

```bash
python -m pytest -v
```

## 📌 Próximos passos

- Desenvolver uma interface web utilizando React.
- Integrar o frontend com a API FastAPI.
- Melhorar a visualização dos resultados da simulação.
- Expandir as funcionalidades do simulador.

## ⚠️ Observação

Este projeto possui finalidade educacional e de demonstração. Não deve ser utilizado como sistema real de assistência ou segurança veicular.

## 👨‍💻 Autor

Desenvolvido por **Murilo Prado** como projeto de estudo e portfólio, com foco em Python, desenvolvimento backend e engenharia de software.