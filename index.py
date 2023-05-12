from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pessoas"
)

# Rota para obter todos os usuários
@app.route('/api/users', methods=['GET'])
def get_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pessoas.pessoa")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

# Rota para obter um usuário específico
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pessoas.pessoa WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return jsonify(user)
    return jsonify({'message': 'Usuário não encontrado'}), 404

# Rota para criar um novo usuário
@app.route('/api/users', methods=['POST'])
def create_user():
    nome = request.json['nome']
    email = request.json['email']
    cursor = db.cursor()
    cursor.execute("INSERT INTO pessoas.pessoa (nome, email) VALUES (%s, %s)", (nome, email))
    db.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return jsonify({'id': user_id, 'nome': nome, 'email': email}), 201

# Rota para atualizar um usuário existente
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    nome = request.json.get('nome')
    email = request.json.get('email')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pessoas.pessoa WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        if nome:
            user['nome'] = nome
        if email:
            user['email'] = email
        cursor.execute("UPDATE pessoas.pessoa SET nome = %s, email = %s WHERE id = %s", (user['nome'], user['email'], user_id))
        db.commit()
        cursor.close()
        return jsonify(user)
    cursor.close()
    return jsonify({'message': 'Usuário não encontrado'}), 404

# Rota para excluir um usuário
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pessoas.pessoa WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute("DELETE FROM pessoas.pessoa WHERE id = %s", (user_id,))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Usuário removido'})
    cursor.close()
    return jsonify({'message': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run()
