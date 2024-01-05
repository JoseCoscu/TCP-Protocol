import socket
import struct

class Package:
    def __init__(self, src, dest, src_port, dest_port, sq_num, ack, flags, window_size, data=b'') -> None:
        self.src= src
        self.dest = dest
        self.src_port = src_port
        self.dest_port = dest_port
        self.sq_num = sq_num
        self.ack = ack
        self.flags = flags
        self.window_size = window_size
        self.data = data
#crear packete en formato binario 
    def pack_header_bin(self):
        ip_header = socket.inet_aton(self.src)
        ip_header += socket.inet_aton(self.dest)
        
        tcp_header = struct.pack('!2h2i2h', self.src_port, self.dest_port,self.sq_num, self.ack, self.flags, self.window_size)
        
        ## TERMINAR DE ARMAR EL HEADER CON EL CHECKSUM YA PUESTO
        ## COMPROBAR ENVIAR UN HEADER CON EL ACK EN EL ACCEPT
        
        return  ip_header, tcp_header
    @staticmethod
    def prepare_checksum_info(self) -> bytes:
        # Construir la pseudo-cabecera
        # if isinstance(self.data, str):
        #     self.data = self.data.encode('utf-8')

        pseudo_header = socket.inet_aton(self.src)
        pseudo_header += socket.inet_aton(self.dest)

        # Construir el encabezado TCP sin el campo de checksum
        tcp_headers_no_checkSum: bytes = struct.pack('!2h2i2h', self.src_port, self.dest_port,
                                         self.sq_num, self.ack, self.flags, self.window_size)
        



        tcp_header: bytes = struct.pack('!2h2i2hi', self.src_port, self.dest_port,
                                         self.sq_num, self.ack, self.flags, self.window_size, 
                                         Package.check_sum(pseudo_header + tcp_headers_no_checkSum + self.data))

        # tcp_header = struct.pack('!HHLLBBHHH', 
        #                          self.src_port, 
        #                          self.dest_port, 
        #                          self.sq_num, 
        #                          self.ack, 
        #                          (5 << 4),  # Longitud del encabezado TCP (5 palabras de 32 bits = 20 bytes) << 4, 0 para reservado
        #                          self.flags, 
        #                          self.window_size)  # Urgent pointer (si se usa)
        # print(tcp_header)
        
        # # Asegurar que la longitud total sea par
        # if len(self.data) % 2 != 0:
        #     self.data += b'\x00'

        # Unir todo para el cálculo del checksum
        return pseudo_header + tcp_header + self.data
    

    ## Modificar checsum !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    @staticmethod
    def check_sum(info: bytes) -> int:
        start: int = 0
        ans: int = 0

        while(start < len(info)):
            ans += int.from_bytes(info[start: start + 2], "little")
            start += 2

        return abs(ans)

    def build_pck(self):
        inf=Package.prepare_checksum_info(self)
        
        return inf




p = Package('192.168.1.1','192.168.1.2',0,9,1,1,0,255,b'hello')
# print(Package.check_sum(Package.prepare_checksum_info(p)))
print(p.build_pck()[0])

