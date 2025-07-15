import os
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
import datetime
import mysql.connector
from functools import wraps
from dotenv import load_dotenv
from flask_cors import CORS
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'my_super_secret_key_12345')
CORS(app, origins=["https://todo-react-cursor-backendin-python-nine.vercel.app"], supports_credentials=True)
bcrypt = Bcrypt(app)

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', '1234'),
    'database': os.getenv('MYSQL_DATABASE', 'todoapp')
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': 'No token provided'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data
        except Exception:
            return jsonify({'message': 'Invalid token'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'message': 'All fields required'}), 400
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    db = None
    cursor = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)', (username, email, pw_hash))
        db.commit()
        return jsonify({'message': 'User registered'}), 201
    except mysql.connector.errors.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 409
    except Exception as e:
        return jsonify({'message': 'Server error', 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'All fields required'}), 400
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if not user or not bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = jwt.encode({'id': user['id'], 'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token, 'username': user['username']})

@app.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks WHERE user_id = %s', (current_user['id'],))
    rows = cursor.fetchall()
    for task in rows:
        if task['checklist']:
            try:
                task['checklist'] = json.loads(task['checklist'])
            except Exception:
                task['checklist'] = []
        else:
            task['checklist'] = []
        task['tag'] = task['tag'] if task['tag'] else ''
    cursor.close()
    db.close()
    return jsonify(rows)

@app.route('/api/tasks', methods=['POST'])
@token_required
def add_task(current_user):
    data = request.json
    text = data.get('text')
    description = data.get('description', '')
    tag = data.get('tag', '')
    checklist = json.dumps(data.get('checklist', []))
    if not text:
        return jsonify({'message': 'Task text required'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO tasks (user_id, text, description, tag, checklist, completed, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, 0, NOW(), NOW())', (current_user['id'], text, description, tag, checklist))
    db.commit()
    task_id = cursor.lastrowid
    cursor.close()
    db.close()
    return jsonify({'id': task_id, 'text': text, 'description': description, 'tag': tag, 'checklist': json.loads(checklist), 'completed': False}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    data = request.json
    text = data.get('text')
    description = data.get('description', '')
    completed = data.get('completed', False)
    tag = data.get('tag', '')
    checklist = json.dumps(data.get('checklist', []))
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE tasks SET text = %s, description = %s, completed = %s, tag = %s, checklist = %s, updated_at = NOW() WHERE id = %s AND user_id = %s', (text, description, int(completed), tag, checklist, task_id, current_user['id']))
    db.commit()
    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return jsonify({'message': 'Task not found'}), 404
    cursor.close()
    db.close()
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, current_user['id']))
    db.commit()
    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return jsonify({'message': 'Task not found'}), 404
    cursor.close()
    db.close()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/userinfo', methods=['GET'])
@token_required
def userinfo(current_user):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT username, email, created_at FROM users WHERE id = %s', (current_user['id'],))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)

@app.route('/')
def home():
    return 'Todo API is running!'

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000))) 