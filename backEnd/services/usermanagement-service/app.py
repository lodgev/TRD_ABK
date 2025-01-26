import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Charger les variables d'environnement
if os.environ.get('ENV') != 'production':
    load_dotenv()

# Créer l'application Flask
app = Flask(__name__)

# 🔗 Connexion à PostgreSQL
DB_HOST = os.getenv("DB_HOST", "user-db")
DB_NAME = os.getenv("POSTGRES_DB", "user-db")
DB_USER = os.getenv("POSTGRES_USER", "user-db")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "user-db")

def get_db_connection():
    """Créer une connexion à PostgreSQL"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Récupérer tous les utilisateurs
@app.route('/UserManagementService/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, firstname, lastname, is_verified, createdat FROM public.users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    users_list = [
        {
            "id": str(user[0]),
            "email": user[1],
            "firstName": user[2],
            "lastName": user[3],
            "isVerified": user[4],
            "createdAt": user[5].strftime('%H:%M:%S')
        }
        for user in users
    ]

    return jsonify({"users": users_list})

# Récupérer un utilisateur par ID
@app.route('/UserManagementService/users/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, firstname, lastname, is_verified, createdat FROM public.users WHERE id = %s;", (str(user_id),))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        user_data = {
            "id": str(user[0]),
            "email": user[1],
            "firstName": user[2],
            "lastName": user[3],
            "isVerified": user[4],
            "createdAt": user[5].strftime('%H:%M:%S')
        }
        return jsonify({"user": user_data})
    else:
        return jsonify({"error": "User not found"}), 404

# Ajouter un utilisateur
@app.route('/UserManagementService/users', methods=['POST'])
def create_user():
    required_fields = ['email', 'password', 'firstName', 'lastName', 'isVerified']
    if not request.json or not all(field in request.json for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    new_user = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO public.users (id, email, password, firstname, lastname, is_verified, createdat) 
        VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, now()) RETURNING id;
        """,
        (new_user["email"], new_user["password"], new_user["firstName"], new_user["lastName"], new_user["isVerified"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User created", "id": str(new_id)}), 201

# Supprimer un utilisateur
@app.route('/UserManagementService/users/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM public.users WHERE id = %s RETURNING id;", (str(user_id),))
    deleted_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted_user:
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

# Mettre à jour un utilisateur
@app.route('/UserManagementService/users/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.json:
        return jsonify({"error": "Missing fields"}), 400

    updated_data = request.json
    conn = get_db_connection()
    cur = conn.cursor()

    query = "UPDATE public.users SET "
    updates = []
    values = []

    if "email" in updated_data:
        updates.append("email = %s")
        values.append(updated_data["email"])
    if "password" in updated_data:
        updates.append("password = %s")
        values.append(updated_data["password"])
    if "firstName" in updated_data:
        updates.append("firstname = %s")
        values.append(updated_data["firstName"])
    if "lastName" in updated_data:
        updates.append("lastname = %s")
        values.append(updated_data["lastName"])
    if "isVerified" in updated_data:
        updates.append("is_verified = %s")
        values.append(updated_data["isVerified"])

    if not updates:
        return jsonify({"error": "No fields to update"}), 400

    query += ", ".join(updates) + " WHERE id = %s RETURNING id;"
    values.append(str(user_id))

    cur.execute(query, values)
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated_user:
        return jsonify({"message": "User updated"})
    else:
        return jsonify({"error": "User not found"}), 404

# Vérifier si un utilisateur est adulte
@app.route('/UserManagementService/users/<uuid:user_id>/is_adult', methods=['GET'])
def is_adult(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, firstname, lastname, createdat FROM public.users WHERE id = %s;", (str(user_id),))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Remplacer cette logique par une véritable vérification basée sur l'âge si disponible
    return jsonify({"is_adult": True})

# Démarrer l'application
if __name__ == '__main__':
    if os.environ.get('ENV') == 'production':
        app.run()
    else:
        app.run(host='0.0.0.0', port=6666, debug=True)
