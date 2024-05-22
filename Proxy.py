import time
import zmq
import json
from datetime import datetime
import statistics
import threading

# Configuración del contexto y sockets
context = zmq.Context()

# Recibir datos de los sensores
consumer_receiver = context.socket(zmq.PULL)
#consumer_receiver.bind("tcp://192.168.138.242:5557")
consumer_receiver.bind("tcp://127.0.0.1:5557")

# Enviar datos a la capa Cloud
cloud_sender = context.socket(zmq.PUSH)
#cloud_sender.connect("tcp://192.168.138.242:5558")
cloud_sender.connect("tcp://127.0.0.1:5558")

# Health Check socket
health_check_socket = context.socket(zmq.REP)
#health_check_socket.bind("tcp://localhost:5560")
health_check_socket.bind("tcp://127.0.0.1:5560")

# Variables para almacenar datos y cálculos
temps_guardadas = []
humedades_guardadas = []
humedades_diarias_guardadas = []
hora_ultima_temp_guardada = time.time()
hora_ultima_humedad_guardada = time.time()

def validar_datos(data):
    """Valida que los datos recibidos no contengan errores."""
    if data['num'] < 0:
        return False
    return True

def calcular_promedio_temperatura():
    """Calcula y envía el promedio de las temperaturas recibidas."""
    global temps_guardadas
    if temps_guardadas:
        temp_prom = statistics.mean(temps_guardadas)
        print(f"Promedio de temperatura: {temp_prom}°C")
        if temp_prom > 29.4:
            enviar_alerta("Temperatura", temp_prom)
        enviar_a_nube("Promedio_Temperatura", temp_prom)
        temps_guardadas = []

def calcular_humedad_diaria():
    """Calcula y envía la humedad diaria."""
    global humedades_guardadas
    if humedades_guardadas:
        humedad_prom = statistics.mean(humedades_guardadas)
        print(f"Promedio de humedad diaria: {humedad_prom}%")
        humedades_diarias_guardadas.append(humedad_prom)
        enviar_a_nube("Humedad_Diaria", humedad_prom)
        humedades_guardadas = []

def enviar_alerta(tipo, valor):
    """Envía una alerta a la nube."""
    mensaje_alerta = {
        'type': tipo,
        'value': valor,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(f"Alerta {tipo}: {valor}")
    cloud_sender.send_json(mensaje_alerta)

def enviar_a_nube(tipo, valor):
    '''Envía datos procesados a la nube.'''
    mensaje = {
        'type': tipo,
        'value': valor,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    cloud_sender.send_json(mensaje)

def health_check():
    while True:
        message = health_check_socket.recv_string()
        print("Message PRoxy: ", message)
        if message == "ping":
            health_check_socket.send_string("pong")
        time.sleep(1)

# Health check thread
threading.Thread(target=health_check).start()

# ------ Main -------

print("Captando mensajes capa Proxy...")

while True:
    work = consumer_receiver.recv_json()
    print(work)
    
    # Validar datos recibidos
    if not validar_datos(work):
        print("Datos inválidos recibidos:", work)
        continue

    # Procesar datos según el tipo de sensor
    if work['name'] == "sensor de temperatura":
        temps_guardadas.append(work['num'])
    elif work['name'] == "sensor de humedad":
        humedades_guardadas.append(work['num'])

    # Calcular promedios y enviar datos a intervalos regulares
    hora_actual = time.time()
    if hora_actual - hora_ultima_temp_guardada >= 6:
        calcular_promedio_temperatura()
        hora_ultima_temp_guardada = hora_actual

    if hora_actual - hora_ultima_humedad_guardada >= 5:
        calcular_humedad_diaria()
        hora_ultima_humedad_guardada = hora_actual
