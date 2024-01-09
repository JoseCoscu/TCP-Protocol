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
    @staticmethod
    def prepare_checksum_info(self) -> bytes:
        # Construir la pseudo-cabecera
        # if isinstance(self.data, str):
        #     self.data = self.data.encode('utf-8')
        pseudo_header = b'\x00\x0f\x00\x0f' 
        pseudo_header += socket.inet_aton(self.src)
        pseudo_header += socket.inet_aton(self.dest)

        # Construir el encabezado TCP sin el campo de checksum
        tcp_headers_no_checkSum: bytes = struct.pack('!2h2i2h', self.src_port, self.dest_port,
                                         self.sq_num, self.ack, self.flags, self.window_size)
        



        tcp_header: bytes = struct.pack('!2h2i2hi', self.src_port, self.dest_port,
                                         self.sq_num, self.ack, self.flags, self.window_size, 
                                         Package.check_sum(pseudo_header + tcp_headers_no_checkSum + self.data))

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
    @staticmethod
    def unzip(pack:bytes)->list:
        tcp_header= struct.unpack('!2h2i2hi', pack[12:32]) 
        tcp_header = list(tcp_header)
        l=list(pack[32:])
        lista = [pack[0:4],socket.inet_ntoa(pack[4:8]),socket.inet_ntoa(pack[8:12])]+tcp_header + list(pack[32:])
        return lista
    