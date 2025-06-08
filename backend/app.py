from flask import Flask, jsonify, request
from flask_cors import CORS # Importa CORS para permitir la comunicación entre frontend y backend

app = Flask(__name__)
CORS(app) # Habilita CORS para todas las rutas

# Simulación de una base de datos en memoria
tasks = []
task_id_counter = 1

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    global task_id_counter
    data = request.json
    if not data or not 'title' in data:
        return jsonify({"error": "Missing title"}), 400

    new_task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'status': 'pending'
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json
    if data:
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        task['status'] = data.get('status', task['status'])
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted"}), 204 # 204 No Content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

