import struct

class BinaryReader:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read(self, fmt):
        size = struct.calcsize(fmt)
        if self.offset + size > len(self.data):
            raise ValueError("Buffer too small to read data")
        value = struct.unpack_from(fmt, self.data, self.offset)
        self.offset += size
        return value

    def read_int32(self):
        return self.read('>i')[0]

    def read_uint16(self):
        return self.read('>H')[0]

    def read_uint32(self):
        return self.read('>I')[0]

    def read_uint8(self):
        return self.read('>B')[0]

    def read_structure_c(self):
        c1 = self.read_int32()
        return c1

    def read_structure_b(self):
        b1 = self.read_structure_c()
        return b1

    def read_structure_a(self):
        if self.offset + 2 > len(self.data):
            raise ValueError("Buffer too small to read data")
        a1_size = self.read_uint16()
        if self.offset + a1_size > len(self.data):
            raise ValueError("Buffer too small to read data")
        a1 = []
        for _ in range(a1_size):
            if self.offset >= len(self.data):
                raise ValueError("Buffer too small to read data")
            a1.append(self.read_uint8())
        a2 = self.read_structure_b()
        return a1, a2
def main(binary_data):
    reader = BinaryReader(binary_data)
    return reader.read_structure_a()



binary_data = b'YKA\xce\x00\x00\x00\x04\x00^\x00\x00\x00b\xbf\xdd6\x9f\xf3\x96v\xf8a1' \
              b'G\xe8O\xb2\xe0\xf2\xdbh\xbe\xcdxQI\x03\x95\xb9\x00\x00\x00n\x00\x00\x00t' \
              b'\x00\x00\x00z?\xe0\x91\xe9\xfe\xd6!*p\xcb\x07\xc4\xbf\xc3\xba\xb5i\xff\xc7p' \
              b'\x00\x04\x00\x00\x00\x80Nu>y\x1e)\xc7\x97\xbe\x1fk\xfc\xbb\xd7\x98 \xf1\xd5' \
              b'\xeb,\x19\x1c\xd6\xa1Z\xa8\xbd\xacz\xd2\x90\xd7\xccNwZ\n=\x1a\xedx\x12' \
              b'iL%\xaep\x8fx\x10[\xac, '

print(main(binary_data))
