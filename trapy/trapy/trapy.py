import socket
from utils import parse_address

class Conn():
    def __init__(self, source, address=None, socke=None):
        if (socke==None):
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        
        self.socket=sock
        self.source = source
        self.address = address 


class ConnException(Exception):
    pass


def listen(address: str) -> Conn:
    connx = Conn(None, address)
    addrs_tuple = parse_address(address)
    connx.socket.bind(addrs_tuple)
    return connx


def accept(conn) -> Conn:
    conn.socket.accept()
    return conn


def dial(address) -> Conn:
    pass


def send(conn: Conn, data: bytes) -> int:
    pass


def recv(conn: Conn, length: int) -> bytes:
    pass


def close(conn: Conn):
    pass
