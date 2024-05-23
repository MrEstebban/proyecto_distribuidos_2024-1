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
consumer_receiver.bind("tcp://10.43.103.80:5557")

# Enviar datos a la capa Cloud
cloud_sender = context.socket(zmq.PUSH)
#cloud_sender.connect("tcp://192.168.138.242:5558")
#cloud_sender.connect("tcp://10.43.103.80:5558")
cloud_sender.connect("tcp://10.195.40.200:5558")

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

def handle_health_check(zmq_socket_health):
    while True:
        try:
            message = zmq_socket_health.recv_json()
            if message.get("type") == "health_check":
                zmq_socket_health.send_json({"status": "alive"})
        except zmq.ZMQError as e:
            print("ZMQ Error:", e)
            break
        time.sleep(1)

# Health check thread
# threading.Thread(target=health_check).start()
zmq_socket_health = context.socket(zmq.REP)
zmq_socket_health.bind("tcp://10.43.103.80:5560")
health_thread = threading.Thread(target=handle_health_check, args=(zmq_socket_health,))
health_thread.start()

# ------ Main -------

print("Captando mensajes capa Proxy Backup...")

while True:
    work = consumer_receiver.recv_json()
    #print(work)
    
    # Validar datos recibidos
    if not validar_datos(work):
        print("Datos inválidos recibidos:", work['name'])
        continue

    

    # Procesar datos según el tipo de sensor
    if work['name'] == "sensor de temperatura":
        if work['alert'] == True:
            print(f"Sensor de temperatura con id {work['id']} envio una alerta")
        temps_guardadas.append(work['num'])
    elif work['name'] == "sensor de humedad":
        if work['alert'] == True:
            print(f"Sensor de humedad con id {work['id']} envio una alerta")
        humedades_guardadas.append(work['num'])
    elif work['name'] == "sensor de humo":
        if work['alert'] == True:
            print(f"Sensor de humo con id {work['id']} activo el aspersor")
        
        

    # Calcular promedios y enviar datos a intervalos regulares
    hora_actual = time.time()
    if hora_actual - hora_ultima_temp_guardada >= 6:
        calcular_promedio_temperatura()
        hora_ultima_temp_guardada = hora_actual

    if hora_actual - hora_ultima_humedad_guardada >= 5:
        calcular_humedad_diaria()
        hora_ultima_humedad_guardada = hora_actual

health_thread.join()
