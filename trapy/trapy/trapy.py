import socket
from package import Package
from utils import parse_address


class Conn:
    def __init__(self, src: str, dest=None, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_RAW)
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
    conn: Conn = Conn(src=address)
    send(conn,b'JoseCoscu',address)
    return conn


def send(conn: Conn, data: bytes, address) -> int:
    conn.socket.sendto(data,parse_address(address))
    return len(data)


def recv(conn: Conn, length: int) -> bytes:
    pass


def close(conn: Conn):
    pass


#### Flagsss -->>> 0:NS 1:CWR 2:ECE 3:URG 4:ACK 5:PSH 6:RST 7:SYN 8:FIN

def hand_shake(conn:Conn):
    print("waiting data")
    data, adrrs = conn.socket.recvfrom(512)
    
    l=Package.unzip(data,data)
    print("PKG recivido")
    
    if (l[22] & 1<<7):
        print("SYN recivido")
        print("enviar ACK SYN")
        send()

    print("PKG recivido")
    print(l)
    
    return
