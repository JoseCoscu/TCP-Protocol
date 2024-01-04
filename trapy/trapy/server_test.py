from socket_trapy import listen, accept, recv, close
addr = '192.168.223.37:9999'
s = listen(addr)
s = accept(s)
print('accepted')
while True:
    rec = recv(s, 255)
    r = rec.decode('utf-8')
    print(r)
    if r == 'close':
        close(s)
        break
