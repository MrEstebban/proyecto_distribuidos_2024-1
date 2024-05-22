import time
import zmq
import json
from datetime import datetime
import statistics
import threading

context = zmq.Context()
consumer_receiver = context.socket(zmq.PULL)

# Backup proxy listens on a different port
#consumer_receiver.bind("tcp://localhost:5559")  
consumer_receiver.bind("tcp://127.0.0.1:5559")

cloud_sender = context.socket(zmq.PUSH)
cloud_sender.connect("tcp://127.0.0.1:5558")

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
    proxy_check_socket = context.socket(zmq.REQ)
    #proxy_check_socket.connect("tcp://localhost:5560")
    proxy_check_socket.connect("tcp://127.0.0.1:5560")

    while True:
        proxy_check_socket.send_string("ping")
        try:
            time.sleep(2)
            message = proxy_check_socket.recv_string(flags=zmq.NOBLOCK)
            print("Message PRoxy_backup: ", message)
            if message != "pong":
                raise zmq.error.Again
        except zmq.error.Again:
            print("Proxy principal no responde, tomando el control...")
            backup_proxy()
            break
        #time.sleep(2)

def backup_proxy():
    global consumer_receiver
    #consumer_receiver.unbind("tcp://localhost:5559")
    #consumer_receiver.bind("tcp://localhost:5557")
    consumer_receiver.unbind("tcp://127.0.0.1:5559")
    consumer_receiver.bind("tcp://127.0.0.1:5557")

threading.Thread(target=health_check).start()

# ------ Main -------

print("Captando mensajes en el proxy de respaldo...")

while True:
    work = consumer_receiver.recv_json()
    print(work)
    
    if not validar_datos(work):
        print("Datos inválidos recibidos:", work)
        continue

    if work['name'] == "sensor de temperatura":
        temps_guardadas.append(work['num'])
    elif work['name'] == "sensor de humedad":
        humedades_guardadas.append(work['num'])

    current_time = time.time()
    if current_time - hora_ultima_temp_guardada >= 6:
        calcular_promedio_temperatura()
        hora_ultima_temp_guardada = current_time

    if current_time - hora_ultima_humedad_guardada >= 5:
        calcular_humedad_diaria()
        hora_ultima_humedad_guardada = current_time
