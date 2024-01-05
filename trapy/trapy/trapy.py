import socket
from utils import parse_address


class Conn:
    def __init__(self, src: str, dest=None, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_TCP)
        self.socket = sock
        self.src = src
        self.dest = dest
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
    pass


def dial(address) -> Conn:
    conn: Conn = Conn(src=address)
    send(conn,b'a',address)
    return conn


def send(conn: Conn, data: bytes, address) -> int:
    conn.socket.sendto(data,parse_address(address))
    return len(data)


def recv(conn: Conn, length: int) -> bytes:
    pass


def close(conn: Conn):
    pass

def hand_shake(conn:Conn):
    print("waiting data")
    data, adrrs = conn.socket.recvfrom(512)
    print (data,adrrs)
    return