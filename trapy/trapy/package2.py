import socket, struct
def tcp_checksum(src_ip, dest_ip, tcp_header, data):
    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(src_ip),
                                socket.inet_aton(dest_ip),
                                0,  # reserved, must be zero
                                socket.IPPROTO_TCP,
                                len(tcp_header) + len(data))

    total = pseudo_header + tcp_header + data
    checksum = 0

    # Suma de 16 bits
    for i in range(0, len(total), 2):
        if i + 1 < len(total):
            word = total[i] + (total[i+1] << 8)
        else:
            word = total[i]
        checksum += word

    # Complemento de uno y recortar a 16 bits
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff
    return checksum



#TCP HEADER
def build_tcp_header(src_port, dest_port, seq_num, ack_num, flags, window_size, src_ip, dest_ip, data):
    # Sin el checksum por ahora
    tcp_header = struct.pack('!HHLLBBHHH', 
                             src_port, dest_port, seq_num, ack_num, 
                             5 << 4, flags, window_size, 0, 0)

    checksum = tcp_checksum(src_ip, dest_ip, tcp_header, data)
    # Reconstruir el encabezado TCP con el checksum
    tcp_header = struct.pack('!HHLLBBH',
                             src_port, dest_port, seq_num, ack_num, 
                             5 << 4, flags, window_size) + \
                 struct.pack('H', checksum) + struct.pack('!H', 0)
    print(tcp_header)
    return tcp_header


#IP HEADER
def build_ip_header(src_ip, dest_ip, tcp_length):
    ip_header = struct.pack('!BBHHHBBH4s4s', 
                            0x45, 0, 20 + tcp_length, 54321, 0, 64, socket.IPPROTO_TCP, 0, 
                            socket.inet_aton(src_ip), socket.inet_aton(dest_ip))
    return ip_header


class Package:
    def __init__(self, src_ip, dest_ip, src_port, dest_port, seq_num, ack_num, flags, window_size, data):
        self.src_ip= src_ip
        self.dest_ip = dest_ip
        self.src_port = src_port
        self.dest_port = dest_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.flags = flags
        self.window_size = window_size
        self.data = data

    def build_pkg(self):
        tcp_header = build_tcp_header(self.src_port, self.dest_port, self.seq_num, self.ack_num, self.flags, self.window_size, self.src_ip, self.dest_ip, self.data)
        ip_header = build_ip_header(self.src_ip, self.dest_ip, len(tcp_header) + len(self.data))
        packet = ip_header + tcp_header + self.data
        return packet
