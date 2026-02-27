from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="terraform-20260227050138453100000001.cr2a4444ubai.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Password123",
        database="userdb"
    )

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username,password) VALUES (%s,%s)", (username,password))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username,password))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})

@app.route('/')
def home():
    return "Signup/Login App Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)