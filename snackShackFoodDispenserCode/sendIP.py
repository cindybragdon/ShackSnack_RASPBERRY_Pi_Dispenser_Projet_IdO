import socket  # Module pour la communication réseau
import time  # Module pour gérer les pauses dans l'exécution

def get_ip():
    """
    Récupère l'adresse IP locale de la machine en se connectant à un serveur externe.
    Utilise Google DNS (8.8.8.8) pour déterminer l'IP.
    
    Returns:
        str: L'adresse IP locale ou "0.0.0.0" en cas d'échec.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Création d'un socket UDP
    s.settimeout(0)  # Définit un timeout à 0 (mode non-bloquant)
    try:
        s.connect(("8.8.8.8", 80))  # Se connecte au serveur DNS de Google
        return s.getsockname()[0]  # Retourne l'adresse IP locale de l'interface utilisée
    except Exception:
        return "0.0.0.0"  # Retourne une IP par défaut si une erreur survient


def broadcast_ip():
    """
    Diffuse périodiquement l'adresse IP locale en broadcast sur le réseau.
    Envoie l'IP sur l'adresse de broadcast 255.255.255.255 via le port 5005.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Création d'un socket UDP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Active l'option broadcast

    while True:
        ip_address = get_ip()  # Récupère l'adresse IP locale
        print("🛜   IP address : " + ip_address)  # Affiche l'adresse IP dans la console
        s.sendto(ip_address.encode(), ("255.255.255.255", 5005))  # Envoie en broadcast
        time.sleep(10)  # Attend 10 secondes avant de renvoyer l'IP
