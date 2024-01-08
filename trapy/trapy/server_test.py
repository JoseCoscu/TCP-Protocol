#from socket_trapy import listen, accept, recv, close
from trapy import listen, hand_shake, accept, recv
import socket
addr = '127.0.0.1:0'

conn = listen(addr)
conn = accept(conn)

recv(conn, 255)






# s = listen(addr)
# s = accept(s)
# print('accepted')
# while True:
#     rec = recv(s, 255)
#     r = rec.decode('utf-8')
#     print(r)
#     if r == 'close':
#         close(s)
#         break
