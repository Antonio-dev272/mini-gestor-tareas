import pytest
import os
import json
from app import app, get_db # Importa app y get_db de tu app.py

# Define una base de datos de prueba diferente para evitar conflictos con la base de datos de desarrollo
TEST_DATABASE = 'test_tasks.db'

# Fixture de pytest para configurar la aplicación y la base de datos para cada test
@pytest.fixture
def client():
    app.config['TESTING'] = True # Activa el modo de prueba de Flask
    app.config['DATABASE'] = TEST_DATABASE # Usa la base de datos de prueba

    # Limpia la base de datos de prueba antes de cada test para asegurar un estado limpio
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)

    with app.app_context():
        # Conecta y crea la tabla de tareas en la base de datos de prueba
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Por hacer'
            )
        ''')
        db.commit()

    # Crea un cliente de prueba de Flask para hacer solicitudes a la aplicación
    with app.test_client() as client:
        yield client # Cede el control al test que usa este fixture

    # Limpia la base de datos de prueba después de cada test
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)

# --- Pruebas de los Endpoints de la API ---

def test_get_tasks_empty(client):
    """Prueba que el endpoint GET /api/tasks devuelve una lista vacía inicialmente."""
    rv = client.get('/api/tasks')
    assert rv.status_code == 200
    assert json.loads(rv.data) == []

def test_add_task(client):
    """Prueba que se puede agregar una tarea vía POST /api/tasks."""
    task_data = {'title': 'Comprar víveres'}
    rv = client.post('/api/tasks', json=task_data)
    assert rv.status_code == 201
    response_data = json.loads(rv.data)
    assert response_data['message'] == 'Tarea agregada'
    assert 'id' in response_data # Verifica que se devuelve un ID
    assert response_data['title'] == 'Comprar víveres'
    assert response_data['status'] == 'Por hacer'

    # Verifica que la tarea aparece al hacer un GET
    rv = client.get('/api/tasks')
    tasks = json.loads(rv.data)
    assert len(tasks) == 1
    assert tasks[0]['title'] == 'Comprar víveres'

def test_add_task_no_title(client):
    """Prueba que no se puede agregar una tarea sin título."""
    rv = client.post('/api/tasks', json={})
    assert rv.status_code == 400
    assert json.loads(rv.data)['error'] == 'Título de tarea requerido'

def test_delete_task(client):
    """Prueba que se puede eliminar una tarea."""
    # Primero, agrega una tarea para tener algo que eliminar
    add_response = client.post('/api/tasks', json={'title': 'Tarea a eliminar'})
    task_id = json.loads(add_response.data)['id']

    # Luego, intenta eliminarla
    delete_response = client.delete(f'/api/tasks/{task_id}')
    assert delete_response.status_code == 200
    assert json.loads(delete_response.data)['message'] == 'Tarea eliminada'

    # Verifica que la tarea ya no exista
    get_response = client.get('/api/tasks')
    assert json.loads(get_response.data) == []

def test_delete_nonexistent_task(client):
    """Prueba eliminar una tarea que no existe."""
    rv = client.delete('/api/tasks/999') # Intenta eliminar un ID que no existe
    assert rv.status_code == 404
    assert json.loads(rv.data)['error'] == 'Tarea no encontrada'

# Puedes añadir más pruebas aquí para futuras funcionalidades (mover, editar, etc.)