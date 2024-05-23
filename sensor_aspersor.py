import zmq
import threading
import json
from datetime import datetime

data_file = "sensor_humedad_data.json"

def almacenar_datos(data, action):
    """Almacena los datos recibidos en un archivo JSON."""
    data['receivedDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['action'] = action
    try:
        with open(data_file, "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"Error al almacenar datos: {e}")

def aspersor():
    global zmq_socketasp
    zmq_socketasp.bind("tcp://10.43.101.42:5555")
    while True:
        war = zmq_socketasp.recv_json()
        almacenar_datos(war, 'get')
        dat = war['mode']
        if dat == 1:
            print("Iniciando sistema de aspersores")

# ------ Main -------

context = zmq.Context()
zmq_socketasp = context.socket(zmq.PULL)

hilo = threading.Thread(target=aspersor, name="Hilo aspersor")
hilo.start()
hilo.join()
