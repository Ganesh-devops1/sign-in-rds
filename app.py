from flask import Flask, request, render_template_string, redirect
import mysql.connector
import logging
import boto3
import os
import time

app = Flask(__name__)

# ==============================
# CloudWatch Logging Setup
# ==============================

LOG_GROUP = "sign-in-rds-logs"
LOG_STREAM = "app-stream"

logs_client = boto3.client("logs", region_name="ap-south-1")

try:
    logs_client.create_log_group(logGroupName=LOG_GROUP)
except logs_client.exceptions.ResourceAlreadyExistsException:
    pass

try:
    logs_client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
except logs_client.exceptions.ResourceAlreadyExistsException:
    pass


def send_log(message):
    logs_client.put_log_events(
        logGroupName=LOG_GROUP,
        logStreamName=LOG_STREAM,
        logEvents=[
            {
                "timestamp": int(time.time() * 1000),
                "message": message
            }
        ]
    )


# ==============================
# RDS Connection
# ==============================

def get_db_connection():
    return mysql.connector.connect(
        host="terraform-20260227050138453100000001.cr2a4444ubai.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Password123",
        database="userdb"
    )

# ==============================
# HTML Templates
# ==============================

signup_page = """
<h2>Signup</h2>
<form method="POST">
Username: <input type="text" name="username"><br>
Password: <input type="password" name="password"><br>
<input type="submit" value="Signup">
</form>
<a href="/login">Go to Login</a>
"""

login_page = """
<h2>Login</h2>
<form method="POST">
Username: <input type="text" name="username"><br>
Password: <input type="password" name="password"><br>
<input type="submit" value="Login">
</form>
<a href="/signup">Go to Signup</a>
"""

# ==============================
# Routes
# ==============================

@app.route("/")
def home():
    return redirect("/signup")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username,password) VALUES (%s,%s)", (username, password))
        db.commit()
        cursor.close()
        db.close()

        send_log(f"New user signed up: {username}")
        return "Signup Successful! <a href='/login'>Login</a>"

    return render_template_string(signup_page)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            send_log(f"User logged in: {username}")
            return "Login Successful!"
        else:
            send_log(f"Failed login attempt: {username}")
            return "Invalid Credentials"

    return render_template_string(login_page)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)