import sqlite3
from flask import Flask, jsonify, request, g
from flask_cors import CORS

DATABASE = 'locadora.db'

app = Flask(__name__)
CORS(app) 

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("Banco de dados inicializado com sucesso.")

@app.route('/api/veiculos', methods=['GET'])
def get_veiculos():
    status = request.args.get('status') 
    conn = get_db()
    
    if status:
        cursor = conn.execute("SELECT * FROM Veiculo WHERE status = ?", (status,))
    else:
        cursor = conn.execute("SELECT * FROM Veiculo")
        
    veiculos = [dict(row) for row in cursor.fetchall()]
    return jsonify(veiculos)

@app.route('/api/veiculos', methods=['POST'])
def add_veiculo():
    dados = request.json
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO Veiculo (modelo, placa, capacidade, status, id_rastreador, descricao) VALUES (?, ?, ?, ?, ?, ?)",
            (
                dados['modelo'], 
                dados['placa'], 
                dados.get('capacidade'), 
                dados['status'], 
                dados.get('id_rastreador'),
                dados.get('descricao') 
            )
        )
        conn.commit()
        return jsonify({"mensagem": "Veículo adicionado com sucesso!"}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({"erro": f"Falha ao adicionar veículo. A placa ou ID do rastreador já existe. {e}"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/veiculos/<int:id_veiculo>', methods=['DELETE'])
def delete_veiculo(id_veiculo):
    conn = get_db()
    conn.execute("DELETE FROM Veiculo WHERE id_veiculo = ?", (id_veiculo,))
    conn.commit()
    return jsonify({"mensagem": "Veículo deletado com sucesso!"})

@app.route('/api/veiculos/<int:id_veiculo>/status', methods=['PUT'])
def update_veiculo_status(id_veiculo):
    dados = request.json
    status = dados.get('status')
    
    conn = get_db()
    conn.execute("UPDATE Veiculo SET status = ? WHERE id_veiculo = ?", (status, id_veiculo))
    conn.commit()
    return jsonify({"mensagem": f"Status do veículo {id_veiculo} atualizado para {status}!"})

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM Cliente")
    clientes = [dict(row) for row in cursor.fetchall()]
    return jsonify(clientes)

@app.route('/api/clientes', methods=['POST'])
def add_cliente():
    dados = request.json
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO Cliente (nome, cpf, cnh, telefone) VALUES (?, ?, ?, ?)",
            (dados['nome'], dados['cpf'], dados.get('cnh'), dados.get('telefone'))
        )
        conn.commit()
        return jsonify({"mensagem": "Cliente adicionado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Falha ao adicionar cliente. CPF já existe."}), 400

@app.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    conn = get_db()
    conn.execute("DELETE FROM Cliente WHERE id_cliente = ?", (id_cliente,))
    conn.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso!"})

@app.route('/api/locacoes', methods=['GET'])
def get_locacoes():
    conn = get_db()
    query = """
        SELECT 
            loc.id_locacao, loc.valor, loc.id_veiculo,
            cli.nome AS cliente_nome, 
            vei.placa AS veiculo_placa
        FROM Locacao loc
        JOIN Cliente cli ON loc.id_cliente = cli.id_cliente
        JOIN Veiculo vei ON loc.id_veiculo = vei.id_veiculo
    """
    cursor = conn.execute(query)
    locacoes = [dict(row) for row in cursor.fetchall()]
    return jsonify(locacoes)

@app.route('/api/locacoes', methods=['POST'])
def add_locacao():
    dados = request.json
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO Locacao (id_cliente, id_veiculo, data, valor, forma_pagamento) VALUES (?, ?, ?, ?, ?)",
            (dados['id_cliente'], dados['id_veiculo'], dados['data'], dados['valor'], dados['forma_pagamento'])
        )
        conn.commit()
        return jsonify({"mensagem": "Locação registrada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/locacoes/<int:id_locacao>', methods=['DELETE'])
def delete_locacao(id_locacao):
    conn = get_db()
    conn.execute("DELETE FROM Locacao WHERE id_locacao = ?", (id_locacao,))
    conn.commit()
    return jsonify({"mensagem": "Locação finalizada com sucesso!"})

@app.route('/api/rastreador/<int:id_rastreador>', methods=['GET'])
def get_posicoes(id_rastreador):
    conn = get_db()
    cursor = conn.execute(
        "SELECT latitude, longitude, data_hora FROM Posicoes WHERE id_rastreador = ? ORDER BY data_hora DESC",
        (id_rastreador,)
    )
    posicoes = [dict(row) for row in cursor.fetchall()]
    return jsonify(posicoes)

@app.route('/api/rastreador', methods=['POST'])
def add_posicao():
    dados = request.json 
    
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO Posicoes (id_rastreador, latitude, longitude, data_hora) VALUES (?, ?, ?, datetime('now', 'localtime'))",
            (dados['id_rastreador'], dados['lat'], dados['lon'])
        )
        conn.commit()
        return jsonify({"mensagem": "Posição recebida com sucesso!"}), 201
    except Exception as e:
        print(f"Erro ao inserir posição: {e}") 
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Banco de dados 'locadora.db' já existe ou falhou ao criar: {e}")
        
    app.run(debug=True, port=5000)