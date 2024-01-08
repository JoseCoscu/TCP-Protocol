from trapy import listen, accept, hand_shake
from package import Package
pkg = Package('127.0.0.1','127.0.0.1',9999,9999,1000,0,130,255,b'JOSEEEE').build_pck()
print(Package.unzip(pkg))