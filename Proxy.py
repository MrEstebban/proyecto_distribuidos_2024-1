import time
import zmq

context = zmq.Context()
# recieve work
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.bind("tcp://127.0.0.1:5557")

while True:
    print("hola")
    work = consumer_receiver.recv_json()
    print(work)