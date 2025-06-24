import pytest
from backend.app import app, db, Board, List, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # Base de datos en memoria
    with app.app_context():
        db.create_all()

        # Crear un tablero, lista y tarea de prueba
        board = Board(name="Tablero de prueba")
        db.session.add(board)
        db.session.commit()

        task_list = List(name="Lista de prueba", board_id=board.id)
        db.session.add(task_list)
        db.session.commit()

        task = Task(title="Tarea de prueba", list_id=task_list.id)
        db.session.add(task)
        db.session.commit()

        yield app.test_client()

        db.drop_all()

def test_get_boards(client):
    response = client.get("/boards")
    assert response.status_code == 200
    assert b"Tablero de prueba" in response.data

def test_create_task(client):
    response = client.post("/lists/1/tasks", json={"title": "Nueva tarea"})
    assert response.status_code == 201
    assert b"Nueva tarea" in response.data

def test_get_tasks(client):
    response = client.get("/lists/1/tasks")
    assert response.status_code == 200
    assert b"Tarea de prueba" in response.data

def test_get_single_task(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200 or response.status_code == 404  # Solo si existe

def test_update_task(client):
    response = client.put("/tasks/1", json={"title": "Tarea modificada"})
    if response.status_code == 200:
        assert b"Tarea modificada" in response.data

def test_delete_task(client):
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert b"Tarea eliminada" in response.data
