import struct


def ipv4(addr):
    """ Return human readable IP address """
    return '.'.join(map(str, addr))


class IPv4:
    def __init__(self, raw_data):
        version_header_length = raw_data[0]
        self.version = version_header_length >> 4
        self.header_length = (version_header_length & 15) * 4
        self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        self.src = ipv4(src)
        self.target = ipv4(target)
        self.data = raw_data[self.header_length:]
