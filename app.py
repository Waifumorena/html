import threading
import asyncio
import websockets
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Conexión a la base de datos SQLite
conn = sqlite3.connect('waifusmo_Emy.db')
c = conn.cursor()

# Crear la tabla mensajes si no existe
c.execute('''CREATE TABLE IF NOT EXISTS mensajes
             (mensaje text)''')

# Crear un Lock para proteger el acceso a la base de datos SQLite
lock = threading.Lock()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'czzxczxcxzasfdafa':
            return render_template('admin.html')
        elif username == 'empleado' and password == 'czzxczxcxzasfdafa':
            return render_template('empleado.html')
        else:
            error = 'Credenciales inválidas. Intente de nuevo.'
    return render_template('login.html', error=error)



if __name__ == '__main__':

    # Crear tareas para el servidor Flask y el servidor WebSocket
    tarea_flask = threading.Thread(target=app.run, kwargs={'host': 'localhost', 'port': 5000})

    # Iniciar las tareas en hilos separados
    tarea_flask.start()

    # Esperar a que las tareas finalicen
    tarea_flask.join()

    # Cerrar la conexión a la base de datos SQLite
    conn.close()







