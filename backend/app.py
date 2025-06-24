from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)

# Crear las tablas dentro del contexto de la app
with app.app_context():
    db.create_all()

# Crear un board y listas por defecto si no existen
with app.app_context():
    if not Board.query.first():
        default_board = Board(name="Default")
        db.session.add(default_board)
        db.session.commit()

        # Crear listas por defecto
        for nombre in ["Por hacer", "En progreso", "Completado"]:
            nueva_lista = List(name=nombre, board_id=default_board.id)
            db.session.add(nueva_lista)
        db.session.commit()

# --- Modelos ---
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lists = db.relationship("List", backref="board", cascade="all, delete")

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=True)
    tasks = db.relationship("Task", backref="list", cascade="all, delete")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"), nullable=False)

# --- Rutas API tradicionales ---

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

@app.route("/boards/<int:board_id>", methods=["DELETE", "PUT"])
def modify_board(board_id):
    board = Board.query.get_or_404(board_id)
    if request.method == "DELETE":
        db.session.delete(board)
        db.session.commit()
        return jsonify({"message": "Board eliminado"})
    elif request.method == "PUT":
        data = request.get_json()
        board.name = data.get("name", board.name)
        db.session.commit()
        return jsonify({"id": board.id, "name": board.name})

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

@app.route("/lists/<int:list_id>", methods=["DELETE", "PUT"])
def modify_list(list_id):
    list_obj = List.query.get_or_404(list_id)
    if request.method == "DELETE":
        db.session.delete(list_obj)
        db.session.commit()
        return jsonify({"message": "Lista eliminada"})
    elif request.method == "PUT":
        data = request.get_json()
        list_obj.name = data.get("name", list_obj.name)
        db.session.commit()
        return jsonify({"id": list_obj.id, "name": list_obj.name})

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

@app.route("/tasks/<int:task_id>", methods=["DELETE", "PUT", "PATCH"])
def modify_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarea eliminada"})
    elif request.method == "PUT":
        data = request.get_json()
        task.title = data.get("title", task.title)
        db.session.commit()
        return jsonify({"id": task.id, "title": task.title})
    elif request.method == "PATCH":
        data = request.get_json()
        new_list_id = data.get("list_id")
        if new_list_id:
            task.list_id = new_list_id
            db.session.commit()
            return jsonify({"id": task.id, "title": task.title, "list_id": task.list_id})
        return jsonify({"error": "list_id es requerido"}), 400

# --- NUEVAS RUTAS para el frontend en /api/cards ---

@app.route("/api/cards", methods=["GET", "POST"])
def api_cards():
    if request.method == "GET":
        tasks = Task.query.all()
        return jsonify([
            {
                "id": task.id,
                "text": task.title,
                "list": task.list.name if task.list else ""
            } for task in tasks
        ])

    elif request.method == "POST":
        data = request.get_json()
        title = data.get("text")
        list_name = data.get("list")

        if not title or not list_name:
            return jsonify({"error": "Faltan campos"}), 400

        lista = List.query.filter_by(name=list_name).first()
        if not lista:
            return jsonify({"error": "La lista no existe"}), 404

        task = Task(title=title, list_id=lista.id)
        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "text": task.title,
            "list": list_name
        }), 201

@app.route("/api/cards/<int:card_id>", methods=["PUT", "DELETE"])
def modificar_tarjeta(card_id):
    task = Task.query.get_or_404(card_id)

    if request.method == "PUT":
        data = request.get_json()
        task.title = data.get("text", task.title)

        nueva_lista = List.query.filter_by(name=data.get("list")).first()
        if nueva_lista:
            task.list_id = nueva_lista.id

        db.session.commit()
        return jsonify({
            "id": task.id,
            "text": task.title,
            "list": nueva_lista.name if nueva_lista else ""
        })

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarea eliminada"})

# --- Pruebas ---
@app.route("/")
def home():
    return "Mini Gestor de Tareas"

@app.route("/nueva-tarea")
def nueva_tarea():
    return "Crear Nueva Tarea"

# --- Main ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
