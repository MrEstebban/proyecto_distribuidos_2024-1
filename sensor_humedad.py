import threading
from time import sleep
import random
import zmq
import socket
from datetime import datetime
import json

def cargar_datos(ruta):
    with open(ruta, "r") as contenido:
        info = json.load(contenido)["info"]
        return info

def generar_numero(min, max):
    numero = random.uniform(0,200)
    while min <= numero <= max: 
        numero = random.uniform(0, 200)
    return numero

def sensorHume():
    global zmq_socket
    global shu
    shu += 1
    while True:
        proba = random.random()
        if proba < hume1:
            numero_aleatorio = random.uniform(70, 100)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : False}
        elif proba < hume1 + hume2:
            numero_aleatorio = generar_numero(70,100)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
        else:
            numero_aleatorio = random.uniform(-1, -100)
            print(threading.current_thread().name, " ", numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}

        zmq_socket.send_json(work_message)
        sleep(5)

# ------ Main -------

datos = cargar_datos("configHume.json")
hume1 = datos['hume1']
hume2 = datos['hume2']
hume3 = datos['hume3']

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("tcp://127.0.0.1:5557")
shu = 0
hostname = socket.gethostname()

hilos = []
for i in range(10):
    print("Creando hilo sensorHumedad: " + str(i+1))
    hilo = threading.Thread(target=sensorHume, name="Hilo sensorHumedad " + str(i+1))
    hilos.append(hilo)

for h in hilos:
    h.start()

for h in hilos:
    h.join()
