import threading
from time import sleep
import random
import zmq
import socket
from datetime import datetime
import json

data_file = "sensor_temp_data.json"

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

def generar_numero(min, max):
    numero = random.uniform(0,200)
    while min <= numero <= max: 
        numero = random.uniform(0, 200)
    return numero

def sensorTemp():
    global zmq_socket
    global st
    st += 1
    while True:
        proba = random.random()
        if proba < temp1:
            numero_aleatorio = random.uniform(11, 29.4)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : False}
        elif proba < temp1 + temp2:
            numero_aleatorio = generar_numero(11,29.4)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
        else:
            numero_aleatorio = random.uniform(-1, -100)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}

        zmq_socket.send_json(work_message)
        almacenar_datos(work_message, 'send')
        sleep(6)

# ------ Main -------

datos = cargar_datos("configTemp.json")
temp1 = datos['temp1']
temp2 = datos['temp2']
temp3 = datos['temp3']

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("tcp://10.43.103.80:5557")
st = 0
hostname = socket.gethostname()

hilos = []
for i in range(10):
    print("Creando hilo sensorTemp: " + str(i+1))
    hilo = threading.Thread(target=sensorTemp, name="Hilo sensorTemp " + str(i+1))
    hilos.append(hilo)

for h in hilos:
    h.start()

for h in hilos:
    h.join()
