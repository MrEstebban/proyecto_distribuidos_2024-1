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

def sensorHumo():
    global zmq_socket
    global sh
    global zmq_socketaspAlert
    sh += 1
    while True:
        proba = random.random()
        if proba < humo1:
            numero_aleatorio = random.choice([0, 1])
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : False}
            if(numero_aleatorio == 1):
                #zmq_socketaspAlert.connect("tcp://192.168.138.242:5555")
                zmq_socketaspAlert.connect("tcp://127.0.0.1:5555")
                alert = { 'mode' : 1}
                work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
                zmq_socketaspAlert.send_json(alert)
        else:
            numero_aleatorio = random.uniform(-1, -100)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
        zmq_socket.send_json(work_message)
        sleep(3)

def sensorTemp():
    global zmq_socket
    global st
    st += 1
    while True:
        proba = random.random()
        if proba < temp1:
            numero_aleatorio = random.uniform(11, 29.4)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : False}
        elif proba < temp1+temp2:
            numero_aleatorio = generar_numero(11,29.4)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
        else:
            numero_aleatorio = random.uniform(-1, -100)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}

        zmq_socket.send_json(work_message)
        sleep(6)
             

def sensorHume():
    global zmq_socket
    global shu
    shu += 1
    while True:
        proba = random.random()
        if proba < hume1:
            numero_aleatorio = random.uniform(70, 100)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : False}
        elif proba < hume1+hume2:
            numero_aleatorio = generar_numero(70,100)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}
        else:
            numero_aleatorio = random.uniform(-1, -100)
            print(threading.current_thread().name, " ",  numero_aleatorio)
            work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'alert' : True}

        zmq_socket.send_json(work_message)
        sleep(5)

def aspersor():
    global zmq_socketasp
    #zmq_socketasp.bind("tcp://192.168.138.242:5555")
    zmq_socketasp.bind("tcp://127.0.0.1:5555")
    while True:
        war = zmq_socketasp.recv_json()
        dat = war['mode']
        if dat == 1:
            print("Iniciando sistema de aspersores")

# ------ Main -------

datos = cargar_datos("configHume.json")
print(datos)
hume1 = datos['hume1']
hume2 = datos['hume2']
hume3 = datos['hume3']

datos = cargar_datos("configTemp.json")
print(datos)
temp1 = datos['temp1']
temp2 = datos['temp2']
temp3 = datos['temp3']

datos = cargar_datos("configHumo.json")
print(datos)
humo1 = datos['humo1']
humo2 = datos['humo2']

print("Valores de hume1, hume2 y hume3:", hume1, hume2, hume3)
print("Valores de temp1, temp2 y temp3:", temp1, temp2, temp3)
print("Valores de humo1 y humo2:", humo1, humo2)

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
#zmq_socket.connect("tcp://192.168.138.242:5557")
zmq_socket.connect("tcp://127.0.0.1:5557")
zmq_socketasp = context.socket(zmq.PULL)
zmq_socketaspAlert = context.socket(zmq.PUSH)
sh = 0
st = 0
shu = 0
hostname = socket.gethostname()

hilo = threading.Thread(target=aspersor, name="Hilo aspersor")
hilo.start()

hilos = []
for i in range(10):
    print("Creando hilo: " + str(i))
    hilo1 = threading.Thread(target=sensorTemp, name="Hilo sensorTemp " + str(i+1))
    hilo2 = threading.Thread(target=sensorHume, name="Hilo sensorHumedad " + str(i+1))
    hilo3 = threading.Thread(target=sensorHumo, name="Hilo sensorHumo " + str(i+1))    
    hilos.extend([hilo1, hilo2, hilo3])

for h in hilos:
    h.start()

for h in hilos:
    h.join()