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

from package import Package
from utils import *
from trapy import send,Conn


# s=dial(addr)
addrs= '127.0.0.1:9999'
conn = Conn(addrs)
pkg = Package('127.0.0.1','127.0.0.2',9999,9999,1,1,128,255,b'JoseCoscu')
pkg = pkg.build_pck()
send(conn,pkg,addrs)
print ("PKG enviado")

#dial('127.0.0.1:9999')



#pkg = Package('192.168.1.1','192.168.1.2',0,9,1,1,0,255,b'hello')

