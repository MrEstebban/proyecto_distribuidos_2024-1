import zmq
import threading

def aspersor():
    global zmq_socketasp
    zmq_socketasp.bind("tcp://127.0.0.1:5555")
    while True:
        war = zmq_socketasp.recv_json()
        dat = war['mode']
        if dat == 1:
            print("Iniciando sistema de aspersores")

# ------ Main -------

context = zmq.Context()
zmq_socketasp = context.socket(zmq.PULL)

hilo = threading.Thread(target=aspersor, name="Hilo aspersor")
hilo.start()
hilo.join()