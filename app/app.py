from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "todos.json"


def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(load_todos())


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todos = load_todos()
    todo = {
        "id": int(datetime.now().timestamp() * 1000),
        "text": data.get("text", "").strip(),
        "done": False,
        "priority": data.get("priority", "medium"),
        "created": datetime.now().strftime("%b %d, %Y")
    }
    if not todo["text"]:
        return jsonify({"error": "Empty task"}), 400
    todos.append(todo)
    save_todos(todos)
    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    todos = load_todos()
    data = request.get_json()
    for todo in todos:
        if todo["id"] == todo_id:
            if "done" in data:
                todo["done"] = data["done"]
            if "text" in data:
                todo["text"] = data["text"]
            save_todos(todos)
            return jsonify(todo)
    return jsonify({"error": "Not found"}), 404


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todos = load_todos()
    todos = [t for t in todos if t["id"] != todo_id]
    save_todos(todos)
    return jsonify({"success": True})


@app.route("/api/todos/clear-done", methods=["DELETE"])
def clear_done():
    todos = load_todos()
    todos = [t for t in todos if not t["done"]]
    save_todos(todos)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
