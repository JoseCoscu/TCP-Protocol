import socket
from package import Package
from utils import parse_address, get_host_ip
import time
import random
import math as m

PKG_SIZE = 30
WINDOW_SIZE = 5
SYN = 1<<7
ACK = 1<<4
FIN = 1<<8
RST = 1<<6

class Conn:
    def __init__(self, src: str, dest=None, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_RAW)
            #sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket = sock
        self.src = src
        self.dest = dest
        self.ack=0
        self.numseq=0
        self.buff = b''
    def __repr__(self) -> str:
        return f'source:{self.src}\n dest:{self.dest}\n ack: {self.ack}\n sqnum: {self.numseq}'

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
    print("HandShake succesfull!!!!!")
    
    return conn


def dial(address) -> Conn:
    #se crea pakt syn y se envia a la direeccion de destino
    hostD,portD=parse_address(address)
    
    ip="127.0.0.1"#get_host_ip()

    print("ip: ",ip)
    conn = Conn(f'{ip}:{portD}') 
    conn.numseq = random.randint(1,100)
    pkg = Package(ip, hostD, portD, portD, conn.numseq,0,SYN,255,b'').build_pck()
    print(Package.unzip(pkg))
    conn.socket.sendto(pkg,parse_address(address))
    time.sleep(1)
    conn = listen(f'{ip}:{portD}')
    print("Esperando data")
    data, _ = conn.socket.recvfrom(255)
    data = Package.unzip(data[20:])
    conn.numseq=data[5]
    conn.ack=data[4]+1
    print(data)

    # if(data[6] & RST):
    #     return print("no enviaste un segmento syn")
    # elif(conn.numseq+1==data[5]):
    #     return print("safasfafasffe")

    pkg_ack=Package(ip,hostD,portD,portD,conn.numseq,conn.ack,ACK,255,b'').build_pck()
    print(Package.unzip(pkg_ack))
    conn.socket.sendto(pkg_ack,parse_address(address))
    

    print("Conexion establecida")

    return conn


def send(conn: Conn, data: bytes, address) -> int:
    #conn.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    data_len = len(data)
    max_data=PKG_SIZE-28
    if(data_len<=max_data):
       hostD,portD=parse_address(conn.src)
       hostS, portS = parse_address(address)
       pkg = Package(hostD,hostS,portD,portS,conn.numseq,conn.ack, ACK, WINDOW_SIZE, data ).build_pck()
       
       print (pkg)
       return conn.socket.sendto(pkg,parse_address(address))

    
    
    data_list = []
    index = 0
    cant=1
    num_pkg = m.ceil(data_len / (max_data))
    while cant <= num_pkg:
        data_list.append(data[index:max_data+index])
        cant+=1
        index+=max_data

    for i in data_list:
        send(conn, i, address)
        conn.ack+=1
        conn.numseq+=1


    
    return len(data)


def recv(conn: Conn, length: int) -> bytes:
    print("esperando datos")
    data, _ = conn.socket.recvfrom(65565)
    data = Package.unzip(data[20:])
    print(data)
    return 


def close(conn: Conn):
    pass



#### Flagsss -->>> 0:NS 1:CWR 2:ECE 3:URG 4:ACK 5:PSH 6:RST 7:SYN 8:FIN
####pakt
def hand_shake(conn:Conn):
    print("waiting data")
    data, _ = conn.socket.recvfrom(65565)
    data=data[20:]
    pkg=Package.unzip(data)

    if(pkg[8] == Package.check_sum(data[:24]+data[28:])):
        print("PKG recivido")
        conn.dest = f'{pkg[1]:}:{pkg[3]}'
        hostS,portS = parse_address(conn.src)
        hostD,portD = parse_address(conn.dest)
        _dest = parse_address(conn.dest)
        if (pkg[6] & SYN):
            print("PKG SYN recivido")
            conn.numseq = random.randint(1,100)
            packSINACK=Package(hostS,hostD,portS,portD,conn.numseq,pkg[4]+1,144,255,b'').build_pck()
            time.sleep(1.5)
            print("Enviando ack/syn")
            conn.socket.sendto(packSINACK,_dest)
            
        else:
            packRST=Package(hostS,hostD,portS,portD,0,0,RST,255,b'').build_pck()
            time.sleep(1.5)
            conn.socket.sendto(packRST, _dest)

    
    data_ack, _ = conn.socket.recvfrom(65565)
    data_ack = Package.unzip(data_ack[20:])
    print(data_ack)
    conn.ack = data_ack[5]
    conn.numseq = data_ack[4]

    return conn
