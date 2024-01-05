#from socket_trapy import listen, accept, recv, close
from trapy import listen, hand_shake
addr = '127.0.0.1:9999'

conn = listen(addr)

hand_shake(conn)






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
