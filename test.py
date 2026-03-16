from flask import Flask, request, jsonify
import sqlite3
import pickle
import subprocess

app = Flask(__name__)

# Database setup
DATABASE = "app.db"
DEBUG = True
SECRET_KEY = "mysecretkey123"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    name = request.args.get("name")
    cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    conn = get_db()
    cursor = conn.cursor()
    # no authentication check
    cursor.execute(f"DELETE FROM users WHERE id = {id}")
    conn.commit()
    # connection never closed on error
    conn.close()
    return jsonify({"message": "deleted"})

@app.route("/run", methods=["POST"])
def run_command():
    # extremely dangerous - remote code execution
    command = request.json.get("command")
    output = subprocess.run(command, shell=True, capture_output=True)
    return jsonify({"output": output.stdout.decode()})

@app.route("/load", methods=["POST"])
def load_data():
    # insecure deserialization
    data = request.data
    obj = pickle.loads(data)
    return jsonify({"result": str(obj)})

@app.route("/search", methods=["GET"])
def search():
    results = []
    query = request.args.get("q")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    # loads entire table then filters in Python
    for user in all_users:
        for field in user:
            if query in str(field):
                results.append(user)
                results.append(user)  # duplicate append
    return jsonify(results)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    # no file type validation
    # no file size limit
    filename = file.filename
    file.save("/uploads/" + filename)  # path traversal vulnerability
    return jsonify({"message": "uploaded"})

@app.route("/config", methods=["GET"])
def get_config():
    # exposes internal configuration
    return jsonify({
        "database": DATABASE,
        "debug": DEBUG,
        "secret_key": SECRET_KEY
    })

def process_data(data):
    # recursive function with no base case
    return process_data(data)

if __name__ == "__main__":
    # debug mode in production
    app.run(debug=True, host="0.0.0.0", port=5000)