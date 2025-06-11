<<<<<<< HEAD
# tests/test_app.py
import pytest

from app import app

@pytest.fixture
def client():
    
    app.config[TESTING] = True
  
    with app.test_client() as client:
        yield client

def test_homepage(client): 
   
    response = client.get('/')
    assert response.status_code == 200 
    assert b Mini Gestor de Tareas in response.data

def test_task_creation_page(client):
   
  
    response = client.get(new_task)
    assert response.status_code == 200
   
    assert b Crear Nueva Tarea in response.data

=======
from app import app  # Asegúrate que app.py tiene "app = Flask(__name__)"

def test_home_route():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
>>>>>>> 30338b4efc012c037c6d93fed5ab9beb1b8e39bb
