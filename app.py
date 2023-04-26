# -*- coding: utf-8 -*-
import threading
import asyncio
import websockets
import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Conexión a la base de datos MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="waifusmo@localhost",
  password="Yasuo123-",
  database="waifusmo_Emy"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return render_template('admin.html')
        elif username == 'empleado' and password == 'empleado':
            return render_template('empleado.html')
        else:
            error = 'Credenciales inválidas. Intente de nuevo.'
    return render_template('login.html', error=error)


# Dirección IP del servidor
HOST = '127.0.0.1'
# Puerto en el que se ejecutará el servidor
PORT = 5001

# Lista de clientes conectados al servidor
clientes = set()

async def manejar_cliente(websocket, path):
    # Agregar el cliente a la lista de clientes
    clientes.add(websocket)

    # Manejar los mensajes del cliente
    async for mensaje in websocket:
        # Enviar el mensaje a todos los clientes conectados
        for cliente in clientes:
            await cliente.send(mensaje)

        # Guardar el mensaje en la base de datos MySQL
        cursor = mydb.cursor()
        sql = "INSERT INTO mensajes (mensaje) VALUES (%s)"
        val = (mensaje,)
        cursor.execute(sql, val)
        mydb.commit()

    # Eliminar el cliente de la lista de clientes
    clientes.remove(websocket)

# Iniciar el servidor WebSocket
async def iniciar_servidor():
    async with websockets.serve(manejar_cliente, HOST, PORT):
        print(f"Servidor escuchando en {HOST}:{PORT}...")
        await asyncio.Future()  # Mantener el servidor en funcionamiento indefinidamente

# Iniciar el servidor Flask y el servidor WebSocket en hilos separados
if __name__ == '__main__':
    hilo_flask = threading.Thread(target=app.run)
    hilo_websockets = threading.Thread(target=asyncio.run, args=(iniciar_servidor(),))

    hilo_flask.start()
    hilo_websockets.start()

    hilo_flask.join()
    hilo_websockets.join()




