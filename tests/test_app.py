from app import app  # Asegúrate que app.py tiene "app = Flask(__name__)"

def test_home_route():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
