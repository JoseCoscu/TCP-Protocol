import socket
from package import Package
from utils import parse_address, get_host_ip
import time


class Conn:
    def __init__(self, src: str, dest=None, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_RAW)
            #sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket = sock
        self.src = src
        self.dest = dest
        self.buff = b''
    def __repr__(self) -> str:
        return f'source:{self.src}\n dest:{self.dest}'

class ConnException(Exception):
    pass

def listen(address: str) -> Conn:
    conn: Conn = Conn(src=address)
    host, port = parse_address(address)
    tuple_addr = (host, port)
    conn.socket.bind(tuple_addr)
    print(f'Listening on {address}')
    return conn


def accept(conn) -> Conn:
    conn = hand_shake(conn)
    return conn


def dial(address) -> Conn:
    #se crea pakt syn y se envia a la direeccion de destino
    hostD,portD=parse_address(address)
    
    ip="127.0.0.1"#get_host_ip()

    print("ip: ",ip)
    conn = Conn(f'{ip}:{portD}')
    pkg = Package(ip,hostD,portD,portD,1000,0,130,255,b'').build_pck()
    send(conn, pkg, address)
    time.sleep(1)
    conn = listen(f'{ip}:{portD}')
    print("esperando data")
    data, _ = conn.socket.recvfrom(255)
    data = data[20:]
    print(Package.unzip(data))

    print("Conexion establecida")

    return conn


def send(conn: Conn, data: bytes, address) -> int:
    #conn.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    conn.socket.sendto(data,parse_address(address))
    return len(data)


def recv(conn: Conn, length: int) -> bytes:
    pass


def close(conn: Conn):
    pass


#### Flagsss -->>> 0:NS 1:CWR 2:ECE 3:URG 4:ACK 5:PSH 6:RST 7:SYN 8:FIN
####pakt
def hand_shake(conn:Conn):
    print("waiting data")
    data, _ = conn.socket.recvfrom(65565)
    data=data[20:]
    l=Package.unzip(data)
    print(l[8])

    if(l[8]==Package.check_sum(data[:24]+data[28:])):
        
        print("PKG recivido")
        if (l[6] & 1<<1):
            print("SYN recivido")
            print(l)
            conn.dest=f'{l[1]:}:{l[3]}'
            hostS,portS=parse_address(conn.src)
            hostD,portD=parse_address(conn.dest)
            packSINACK=Package(hostS,hostD,portS,portD,l[5]+1,l[4]+1,144,255,b'').build_pck()
            time.sleep(1.5)
            print("enviando ack/syn")
            conn.socket.sendto(packSINACK,parse_address(conn.dest))
    #else aceptar la conexion primro 

    return conn
    return
