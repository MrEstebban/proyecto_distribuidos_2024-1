import time
import zmq

context = zmq.Context()
# recieve work
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.bind("tcp://192.168.10.121:5557")
print("Captando mensajes...")
while True:
    work = consumer_receiver.recv_json()
    print(work)