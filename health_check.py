import zmq
import subprocess
import time

def start_proxy_backup():
    subprocess.Popen(['start', 'cmd', '/k', 'python Proxy_backup.py'], shell=True)

def check_health(primary_ip="10.43.103.80", health_port="5560"):
    context = zmq.Context()
    primary_socket = context.socket(zmq.REQ)
    primary_socket.connect(f"tcp://{primary_ip}:{health_port}")  # socket para el puerto de receptor
    primary_socket.RCVTIMEO = 1000  # 1 second timeout

    backup_active = False
    backup_socket = context.socket(zmq.REQ)
    backup_socket.connect(f"tcp://{primary_ip}:{health_port}")  # Port para el health check del backup
    backup_socket.RCVTIMEO = 1000  # 1 sec de timeout

    while True:
        try:
            primary_socket.send_json({"type": "health_check"})
            message = primary_socket.recv_json()
            print(f"Primary proxy health check response: {message}")
        except zmq.Again:
            print("Primary proxy did not respond, assuming failure.")
            if not backup_active:
                print("Activating backup proxy...")
                #corre el backup
                start_proxy_backup()
                backup_active = True
        except zmq.ZMQError as e:
            print(f"Primary proxy failed: {e}")
            if not backup_active:
                print("Activating backup proxy...")
                #corre el backup
                start_proxy_backup()
                backup_active = True

        if backup_active:
            try:
                backup_socket.send_json({"type": "health_check"})
                message = backup_socket.recv_json()
                print(f"Backup proxy health check response: {message}")
            except zmq.Again:
                print("Backup proxy did not respond.")
            except zmq.ZMQError as e:
                print(f"Backup proxy failed: {e}")
                break

        time.sleep(5)  # revisa cada 5 secs

if __name__ == "__main__":
    check_health()
