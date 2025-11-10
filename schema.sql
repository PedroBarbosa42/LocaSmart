CREATE TABLE Veiculo (
    id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo VARCHAR(50) NOT NULL,
    placa VARCHAR(7) UNIQUE NOT NULL,
    capacidade INT,
    status VARCHAR(100) NOT NULL DEFAULT 'Disponível',
    id_rastreador INT UNIQUE,
    descricao TEXT -- NOVA COLUNA PARA A DESCRIÇÃO DA IA
);

CREATE TABLE Cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20) UNIQUE NOT NULL,
    cnh VARCHAR(20),
    telefone VARCHAR(20)
);

CREATE TABLE Locacao (
    id_locacao INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATETIME NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50),
    
    id_cliente INT,
    id_veiculo INT,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_veiculo) REFERENCES Veiculo(id_veiculo)
);

CREATE TABLE Posicoes (
    id_posicao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_rastreador INT NOT NULL, 
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    data_hora DATETIME NOT NULL
);