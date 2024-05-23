import threading
from time import sleep
import random
import zmq
import socket
from datetime import datetime
import json

data_file = "sensor_humo_data.json"

def almacenar_datos(data, action):
    """Almacena los datos recibidos en un archivo JSON."""
    data['receivedDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['action'] = action
    try:
        with open(data_file, "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"Error al almacenar datos: {e}")

def cargar_datos(ruta):
    with open(ruta, "r") as contenido:
        info = json.load(contenido)["info"]
        return info

def sensorHumo():
    global zmq_socket
    global sh
    global zmq_socketaspAlert
    sh += 1
    while True:
        proba = random.random()
        if proba < humo1:
            numero_aleatorio = random.choice([0, 1])
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : False}
            if numero_aleatorio == 1:
                zmq_socketaspAlert.connect("tcp://10.43.101.42:5555")
                alert = { 'mode' : 1}
                work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
                zmq_socketaspAlert.send_json(alert)
                almacenar_datos(alert, 'alert')

        else:
            numero_aleatorio = random.uniform(-1, -100)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
        zmq_socket.send_json(work_message)
        almacenar_datos(work_message, 'send')
        sleep(3)

# ------ Main -------

datos = cargar_datos("configHumo.json")
humo1 = datos['humo1']
humo2 = datos['humo2']

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("tcp://10.43.103.80:5557")
zmq_socketaspAlert = context.socket(zmq.PUSH)
sh = 0
hostname = socket.gethostname()

hilos = []
for i in range(10):
    print("Creando hilo sensorHumo: " + str(i+1))
    hilo = threading.Thread(target=sensorHumo, name="Hilo sensorHumo " + str(i+1))
    hilos.append(hilo)

for h in hilos:
    h.start()

for h in hilos:
    h.join()
