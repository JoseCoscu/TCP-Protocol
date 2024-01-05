from socket_trapy import dial, send, close
addr = '127.0.0.1:9999'
s = dial(addr)
print('Conexion Exitosa')
while True:
    _msg = input()
    msg = _msg.encode('utf-8')
    send(s, msg)
    if _msg == 'close':
        close(s)
        break
