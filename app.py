from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Database file
DATABASE = 'users.db'

# home 
@app.route('/',)

def home():
    return "work"
# Initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        conn.commit()

# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return jsonify({"users": [{"id": user[0], "name": user[1]} for user in users]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({"error": "Name is required"}), 400

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()

        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update a user
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({"error": "Name is required"}), 400

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
            conn.commit()

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete a user
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
