from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para almacenar tareas en memoria
tareas = []

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    if titulo:
        tareas.append(titulo)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:indice>', methods=['POST'])
def eliminar(indice):
    if 0 <= indice < len(tareas):
        tareas.pop(indice)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

