from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)

# MODELOS
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lists = db.relationship("List", backref="board", cascade="all, delete")

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    tasks = db.relationship("Task", backref="list", cascade="all, delete")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"), nullable=False)

# CREAR LA DB
with app.app_context():
    db.create_all()

# RUTAS BOARDS
@app.route("/boards", methods=["GET", "POST"])
def handle_boards():
    if request.method == "POST":
        data = request.get_json()
        new_board = Board(name=data["name"])
        db.session.add(new_board)
        db.session.commit()
        return jsonify({"id": new_board.id, "name": new_board.name}), 201

    boards = Board.query.all()
    return jsonify([{"id": b.id, "name": b.name} for b in boards])

@app.route("/boards/<int:board_id>", methods=["PUT", "DELETE"])
def modify_board(board_id):
    board = Board.query.get_or_404(board_id)

    if request.method == "PUT":
        data = request.get_json()
        board.name = data["name"]
        db.session.commit()
        return jsonify({"id": board.id, "name": board.name})

    if request.method == "DELETE":
        db.session.delete(board)
        db.session.commit()
        return jsonify({"message": "Board eliminado"}), 204

# RUTAS LISTS
@app.route("/boards/<int:board_id>/lists", methods=["GET", "POST"])
def handle_lists(board_id):
    if request.method == "POST":
        data = request.get_json()
        new_list = List(name=data["name"], board_id=board_id)
        db.session.add(new_list)
        db.session.commit()
        return jsonify({"id": new_list.id, "name": new_list.name}), 201

    lists = List.query.filter_by(board_id=board_id).all()
    return jsonify([{"id": l.id, "name": l.name} for l in lists])

@app.route("/lists/<int:list_id>", methods=["PUT", "DELETE"])
def modify_list(list_id):
    list_obj = List.query.get_or_404(list_id)

    if request.method == "PUT":
        data = request.get_json()
        list_obj.name = data["name"]
        db.session.commit()
        return jsonify({"id": list_obj.id, "name": list_obj.name})

    if request.method == "DELETE":
        db.session.delete(list_obj)
        db.session.commit()
        return jsonify({"message": "Lista eliminada"}), 204

# RUTAS TASKS
@app.route("/lists/<int:list_id>/tasks", methods=["GET", "POST"])
def handle_tasks(list_id):
    if request.method == "POST":
        data = request.get_json()
        new_task = Task(title=data["title"], list_id=list_id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"id": new_task.id, "title": new_task.title}), 201

    tasks = Task.query.filter_by(list_id=list_id).all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])

@app.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def modify_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == "PUT":
        data = request.get_json()
        task.title = data["title"]
        db.session.commit()
        return jsonify({"id": task.id, "title": task.title})

    if request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarea eliminada"}), 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

