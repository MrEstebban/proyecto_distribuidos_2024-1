import threading 
from time import sleep
import random
import zmq
import socket
from datetime import datetime

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.connect("tcp://127.0.0.1:5557")
sh = 0
st = 0
shu = 0
hostname = socket.gethostname()

def sensorHumo():
    global zmq_socket
    global sh
    sh += 1
    while True:
        numero_aleatorio = random.choice([0, 1])
        print(threading.current_thread().name, " ",  numero_aleatorio)
        work_message = { 'Hostname' : hostname, 'name' : "sensor de humo", 'id' : sh, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        zmq_socket.send_json(work_message)
        sleep(3)

def sensorTemp():
    global zmq_socket
    global st
    st += 1
    while True:
        numero_aleatorio = random.uniform(11, 29.4)
        print(threading.current_thread().name, " ",  numero_aleatorio)
        work_message = { 'Hostname' : hostname, 'name' : "sensor de temperatura", 'id' : st, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        zmq_socket.send_json(work_message)
        sleep(6)

def sensorHume():
    global zmq_socket
    global shu
    shu += 1
    while True:
        numero_aleatorio = random.uniform(70, 100)
        print(threading.current_thread().name, " ",  numero_aleatorio)
        work_message = { 'Hostname' : hostname, 'name' : "sensor de humedad", 'id' : shu, 'num' : numero_aleatorio, 'date' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        zmq_socket.send_json(work_message)
        sleep(5)

hilo1 = threading.Thread(target=sensorTemp, name="Hilo 1")
hilo2 = threading.Thread(target=sensorHume, name="Hilo 2")
hilo3 = threading.Thread(target=sensorHumo, name="Hilo 3")    

hilo1.start()
hilo2.start()
hilo3.start()

hilo1.join()
hilo2.join()
hilo3.join()

print("Volvi al main")
