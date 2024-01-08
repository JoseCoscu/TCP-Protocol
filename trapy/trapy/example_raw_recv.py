import socket
from package import Package
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

s.bind(('127.0.0.1', 0))
while True:
    data,_ = s.recvfrom(65565)
    data = data[20:]
    print(data)
  

    _data = Package.unzip(data)
    print(_data)
    print('\n-----------------------\n')
