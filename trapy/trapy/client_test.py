# from socket_trapy import dial, send, close
# addr = '127.0.0.1:9999'
# s = dial(addr)
# print('Conexion Exitosa')
# while True:
#     _msg = input()
#     msg = _msg.encode('utf-8')
#     send(s, msg)
#     if _msg == 'close':
#         close(s)
#         break

#from socket_trapy import send, dial
#from package import *
import time
import socket
from package import Package
from utils import *
from trapy import send,Conn,listen, dial

addrs= '127.0.0.1:9999'
conn=dial(addrs)
send(conn,b"Hello world",addrs)

# dial(addrs)

# conn = Conn(addrs)
# pkg = Package('127.0.0.1','127.0.0.1',9999,9999,1000,0,130,255,b'JOSEEEE')

# _pkg = pkg.build_pck()
# print(_pkg)
# send(conn,_pkg,'127.0.0.1:9999')
# print ("PKG enviado")
# time.sleep(1)
# conn=listen(addrs)
# print('esperando data')
# data, _ = conn.socket.recvfrom(65565)
# data=data[20:]
# l=Package.unzip(data)
# print(l)


#dial('127.0.0.1:9999')



#pkg = Package('192.168.1.1','192.168.1.2',0,9,1,1,0,255,b'hello')

