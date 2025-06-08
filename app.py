from flask import Flask, request, jsonify, render_template, g
import sqlite3
import os

app = Flask(__name__)

# Configuración de la base de datos
# Usamos app.config para que podamos cambiarla fácilmente en los tests
app.config['DATABASE'] = 'tasks.db' # Base de datos para la aplicación normal

# --- Funciones para manejo de la Base de Datos ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Conecta a la base de datos especificada en app.config['DATABASE']
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return db

def init_db():
    # Esta función se llama para crear la tabla de tareas si no existe
    with app.app_context(): # Necesitamos un contexto de aplicación para acceder a 'g' y 'app.config'
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

# Cierra la conexión de la base de datos al finalizar cada solicitud o contexto
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Endpoints de la API (Backend) ---

# Ruta para obtener todas las tareas
@app.route('/api/tasks', methods=['GET'])
def get_tasks_api():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = [dict(row) for row in cursor.fetchall()] # Convierte las filas a diccionarios
    return jsonify(tasks)

# Ruta para añadir una nueva tarea
@app.route('/api/tasks', methods=['POST'])
def add_task_api():
    data = request.get_json() # Espera un JSON en el cuerpo de la solicitud
    if not data or 'title' not in data:
        return jsonify({'error': 'Título de tarea requerido'}), 400
    
    title = data['title']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    # Devuelve la tarea recién creada con su ID y estado por defecto
    return jsonify({'message': 'Tarea agregada', 'id': cursor.lastrowid, 'title': title, 'status': 'Por hacer'}), 201

# Ruta para eliminar una tarea por ID
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_api(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cursor.rowcount == 0: # Si no se eliminó ninguna fila, la tarea no existía
        return jsonify({'error': 'Tarea no encontrada'}), 404
    return jsonify({'message': 'Tarea eliminada'}), 200

# --- Rutas para servir el Frontend (archivos estáticos y plantilla principal) ---
# Esta ruta sirve tu `index.html` y luego el JS de ese HTML llamará a las APIs de arriba
@app.route('/')
def index():
    return render_template('index.html')

# Ejecución de la aplicación
if __name__ == '__main__':
    # Asegura que la tabla de la base de datos se cree al iniciar la aplicación
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)


