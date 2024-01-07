import socket
from package import Package
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

s.bind(('192.168.2.37', 0))
while True:
    data = s.recvfrom(65565)[1]
    print(data)
    print('\n-----------------------\n')
