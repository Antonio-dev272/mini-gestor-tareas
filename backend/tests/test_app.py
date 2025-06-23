import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
