import pytest
import json
from app import app

# -------- CONFIGURACIÓN DEL CLIENTE DE PRUEBA --------
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# -------- PRUEBAS PARA TABLEROS (Boards) --------
def test_get_boards_empty(client):
    """Debe devolver una lista vacía si no hay tableros"""
    rv = client.get('/boards')
    assert rv.status_code == 200
    assert json.loads(rv.data) == []

def test_create_board(client):
    """Debe poder crear un tablero con POST"""
    data = {'name': 'Tablero de prueba'}
    rv = client.post('/boards', json=data)
    assert rv.status_code == 201
    result = json.loads(rv.data)
    assert result['name'] == 'Tablero de prueba'
    assert 'id' in result

def test_create_board_missing_name(client):
    """Debe devolver un error si el nombre del tablero está ausente"""
    rv = client.post('/boards', json={})
    assert rv.status_code in (400, 500)

# -------- PRUEBAS PARA LISTAS --------
def test_create_list_and_get_lists(client):
    """Debe poder crear una lista en un tablero y luego obtenerla"""
    # Crear tablero
    board_data = {'name': 'Tablero con listas'}
    rv = client.post('/boards', json=board_data)
    board = json.loads(rv.data)
    board_id = board['id']

    # Crear lista en ese tablero
    list_data = {'name': 'Lista A'}
    rv = client.post(f'/boards/{board_id}/lists', json=list_data)
    assert rv.status_code == 201
    created_list = json.loads(rv.data)
    assert created_list['name'] == 'Lista A'
    assert 'id' in created_list

    # Obtener listas del tablero
    rv = client.get(f'/boards/{board_id}/lists')
    assert rv.status_code == 200
    lists = json.loads(rv.data)
    assert len(lists) == 1
    assert lists[0]['name'] == 'Lista A'

# -------- PRUEBAS PARA TAREAS (Tasks) --------
def test_create_task_and_get_tasks(client):
    """Debe poder crear una tarea en una lista y luego obtenerla"""
    # Crear tablero
    board_data = {'name': 'Tablero con tareas'}
    rv = client.post('/boards', json=board_data)
    board_id = json.loads(rv.data)['id']

    # Crear lista
    list_data = {'name': 'Lista B'}
    rv = client.post(f'/boards/{board_id}/lists', json=list_data)
    list_id = json.loads(rv.data)['id']

    # Crear tarea
    task_data = {'title': 'Tarea 1'}
    rv = client.post(f'/lists/{list_id}/tasks', json=task_data)
    assert rv.status_code == 201
    task = json.loads(rv.data)
    assert task['title'] == 'Tarea 1'
    assert 'id' in task

    # Obtener tareas
    rv = client.get(f'/lists/{list_id}/tasks')
    assert rv.status_code == 200
    tasks = json.loads(rv.data)
    assert len(tasks) == 1
    assert tasks[0]['title'] == 'Tarea 1'
