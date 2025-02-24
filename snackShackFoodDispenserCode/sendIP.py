import socket
import time


#PAS sur si on a besoin de ça
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "0.0.0.0"

def broadcast_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        ip_address = get_ip()
        print("🛜   IP adress : " + ip_address)
        s.sendto(ip_address.encode(), ("255.255.255.255", 5005))
        time.sleep(10)  # Envoie l'IP toutes les 10 secondes
