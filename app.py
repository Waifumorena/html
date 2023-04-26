import threading
import asyncio
import websockets
import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)


mydb = mysql.connector.connect(
  host="localhost",
  user="waifusmo",
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
            error = "Credenciales inválidas. Intente de nuevo."
    return render_template('login.html', error=error)



HOST = '149.56.67.133'

PORT = 5001


clientes = set()

async def manejar_cliente(websocket, path):
    
    clientes.add(websocket)

    
    async for mensaje in websocket:
        
        for cliente in clientes:
            await cliente.send(mensaje)

        
        cursor = mydb.cursor()
        sql = "INSERT INTO mensajes (mensaje) VALUES (%s)"
        val = (mensaje,)
        cursor.execute(sql, val)
        mydb.commit()

    
    clientes.remove(websocket)


async def iniciar_servidor():
    async with websockets.serve(manejar_cliente, HOST, PORT):
        print(f"Servidor escuchando en {HOST}:{PORT}...")
        await asyncio.Future()  


if __name__ == '__main__':
    hilo_flask = threading.Thread(target=app.run(host='149.56.67.133', port=5000))
    hilo_websockets = threading.Thread(target=asyncio.run, args=(iniciar_servidor(),))

    hilo_flask.start()
    hilo_websockets.start()

    hilo_flask.join()
    hilo_websockets.join()



