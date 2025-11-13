# LocaSmart - 🚗 Sistema de Locação de Veículos (Flask + Rastreamento GPS)

Este é um projeto full-stack de um sistema de gerenciamento para uma locadora de veículos. O back-end em Flask (Python) gerencia clientes, veículos e locações, enquanto o front-end (HTML/Tailwind CSS) consome a API.

O projeto se destaca pela funcionalidade de **Rastreamento de Frota**, que simula e exibe a localização de múltiplos veículos em um mapa em tempo real.

## 📍 Principais Funcionalidades

* **Gerenciamento de Clientes:** CRUD (Criar, Ler, Excluir) de clientes.
* **Gerenciamento de Veículos:** CRUD (Criar, Ler, Excluir) de veículos, com campo para descrição manual.
* **Registro de Locações:** Permite registrar uma nova locação, vinculando um cliente a um veículo "Disponível" e alterando seu status para "Alugado".
* **Rastreamento GPS em Tempo Real:** Uma aba "Rastreador" exibe um mapa interativo (com Leaflet.js) que mostra a última localização de qualquer veículo selecionado no dropdown.
* **Simulador de Frota (Multi-Veículos):** Um script (`simulador.py`) que busca *toda* a frota de veículos na API e, em paralelo, envia novas coordenadas GPS para cada um deles, permitindo o monitoramento de múltiplos carros ao mesmo tempo.

## 🛠️ Tecnologias Utilizadas

* **Back-end:**
    * **Python 3**
    * **Flask:** Para a criação da API REST.
    * **SQLite3:** Para o banco de dados.
    * **Flask-CORS:** Para permitir a comunicação entre o front-end e o back-end.
* **Front-end:**
    * **HTML5**
    * **Tailwind CSS:** Para estilização rápida e moderna.
    * **JavaScript (Vanilla):** Para lógica do cliente, navegação SPA (Single Page Application) e chamadas de API (`fetch`).
    * **Leaflet.js:** Biblioteca de mapas interativos.
* **Simulação:**
    * **Requests (Python):** Utilizado no script de simulação (`simulador.py`).

## 🚀 Como Executar o Projeto

Siga estes passos para rodar o sistema completo em sua máquina local.

### Pré-requisitos

* Python 3.x
* (Opcional) Um editor de código como o VS Code.

### 1. Instalação

1.  Clone este repositório:
    ```
    git clone [https://github.com/PedroBarbosa42/LocaSmart.git](https://github.com/PedroBarbosa42/LocaSmart.git)
    cd LocaSmart
    ```
2.  (Opcional, mas recomendado) Crie e ative um ambiente virtual:
    ```
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Instale as dependências do Python:
    ```
    pip install Flask flask-cors requests
    ```

### 2. Executando a Aplicação

Você precisará de **dois terminais** abertos.

#### Terminal 1: Servidor Back-end (Flask)

1.  (Se necessário) Delete o arquivo `locadora.db` para garantir que o banco de dados seja criado com o `schema.sql` mais recente.
2.  Execute o servidor Flask:
    ```
    python app.py
    ```
    *O servidor estará rodando em `http://127.0.0.1:5000` e criará um novo arquivo `locadora.db`.*

#### Navegador: Front-end

1.  Abra o arquivo `index.html` diretamente no seu navegador (clique duplo).
2.  **Teste o Cadastro:**
    * Vá para a aba **"Clientes"** e cadastre alguns clientes.
    * Vá para a aba **"Veículos"** e cadastre alguns veículos.
    * **Importante:** Ao cadastrar veículos, preencha o campo **"ID do Rastreador"** com números únicos (ex: `1`, `2`, `3`).

#### Terminal 2: Simulador de GPS

1.  Abra um **novo terminal** (mantenha o primeiro rodando).
2.  Execute o simulador de múltiplos veículos:
    ```
    python