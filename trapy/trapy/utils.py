import subprocess
import requests
import socket
def parse_address(address):
    host, port = address.split(':')

    if host == '':
        host = 'localhost'

    return host, int(port)



def get_host_ip():
    try:
        # Crea un socket para conectarse a un servidor externo
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # No es necesario establecer una conexión real
            s.connect(("8.8.8.8", 80))
            # Obtener la dirección IP del socket
            ip = s.getsockname()[0]
    except Exception:
        ip = "No se pudo determinar la IP"
    return ip

