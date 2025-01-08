import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request


# Charger les variables d'environnement à partir du fichier .env lorsque nous ne sommes pas en mode production
if os.environ.get('ENV') != 'production':
  load_dotenv()


# Créer une app Flask
app = Flask(__name__)


# Echantillon de données pour travailler
users = [
  {
    'id': 1,
    'firstName': 'Doriane',
    'lastName': 'Bedier',
    'email' : 'doriane.bedier@gmail.com',
    'age': 23
  },
  {
    'id': 2,
    'firstName': 'Olha',
    'lastName': 'Aleynik',
    'email' : 'olha.aleynik@gmail.com',
    'age': 17
  },
  {
    'id': 3,
    'firstName': 'Oleksandra',
    'lastName': 'Kuksa',
    'email' : 'oleksandra.kuksa@gmail.com',
    'age': 23
  }
]


# Route "/UserManagementService/users" (GET) pour lister tous les users
@app.route('/UserManagementService/users', methods=['GET'])
def get_users():
  return jsonify({'users': users})


# Route "/UserManagementService/users/<user_id>" (GET) pour obtenir un user spécifique par son ID
@app.route('/UserManagementService/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
  user = [user for user in users if user['id'] == user_id]
  if len(user) == 0:
    return jsonify({'error': 'User not found'}), 404
  return jsonify({'user': user[0]})


# Route "/UserManagementService/users" (POST) pour créer un nouvel utilisateur
@app.route('/UserManagementService/users', methods=['POST'])
def create_user():
  if not request.json or not 'firstName' or not 'lastName' or not 'email' or not 'age' in request.json:
    return jsonify({'error': 'Infos are required'}), 400
  user = {
    'id': users[-1]['id'] + 1,
    'firstName': request.json['firstName'],
    'lastName': request.json['lastName'],
    'email': request.json['email'],
    'age': request.json['age']
  }
  users.append(user)
  return jsonify({'user': user}), 201


# Route "/UserManagementService/users/<user_id>" (DELETE) pour supprimer un utilisateur
@app.route('/UserManagementService/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    users = [u for u in users if u['id'] != user_id]
    return jsonify({'message': f'User {user_id} deleted successfully'}), 200


@app.route('/UserManagementService/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    if 'firstName' in data:
        user['firstName'] = data['firstName']
    if 'lastName' in data:
        user['lastName'] = data['lastName']
    if 'email' in data:
        user['email'] = data['email']
    if 'age' in data:
        user['age'] = data['age']

    return jsonify({'user': user}), 200


# Enfin, démarrer l'API
if __name__ == '__main__':
  if os.environ.get('ENV') == 'production':
    app.run()
  else:
    app.run(host='0.0.0.0', port=6666, debug=True)