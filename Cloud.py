import zmq
import json
from datetime import datetime
import statistics

# Configuración del contexto y sockets
context = zmq.Context()

# Recibir datos y alertas desde la capa Fog
cloud_receiver = context.socket(zmq.PULL)
#cloud_receiver.bind("tcp://192.168.138.242:5558")
cloud_receiver.bind("tcp://10.43.103.80:5558")

# Variables para almacenar datos
valores_humedad_mensual = []
valores_humedad_diaria = []

# Archivo de almacenamiento
data_file = "cloud_data.json"

def almacenar_datos(data):
    """Almacena los datos recibidos en un archivo JSON."""
    try:
        with open(data_file, "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"Error al almacenar datos: {e}")

def calcular_humedad_mensual():
    """Calcula y almacena la humedad relativa mensual."""
    if valores_humedad_diaria:
        humedad_mensual_prom = statistics.mean(valores_humedad_diaria)
        valores_humedad_mensual.append(humedad_mensual_prom)
        print(f"Humedad relativa mensual: {humedad_mensual_prom}%")
        almacenar_datos({
            'type': 'Humedad_Mensual',
            'value': humedad_mensual_prom,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        valores_humedad_diaria.clear()
        if humedad_mensual_prom < 70:
            enviar_alerta("Humedad_Mensual", humedad_mensual_prom)

def enviar_alerta(tipo, valor):
    """Genera una alerta si los valores están fuera de los límites permitidos."""
    mensjae_alerta = {
        'type': tipo,
        'value': valor,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(f"Alerta {tipo}: {valor}")
    almacenar_datos(mensjae_alerta)

# ------ Main -------

print("Captando mensajes en la capa Cloud...")

while True:
    work = cloud_receiver.recv_json()
    print(work)

    # Almacenar todos los datos recibidos
    almacenar_datos(work)

    # Procesar datos de humedad diaria para calcular humedad mensual
    if work['type'] == "Humedad_Diaria":
        valores_humedad_diaria.append(work['value'])
    
    # Calcular humedad mensual cada 20 segundos (para efectos de la simulación)
    if len(valores_humedad_diaria) >= 4:  # Suponiendo 4 valores diarios para simplificación
        calcular_humedad_mensual()
