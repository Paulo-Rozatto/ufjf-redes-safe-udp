import zlib

TYPE = {
    "DATA": 1,
    "ACK": 2,
    "NAK": 3,
    "FIN": 4,
}

TYPE_CONVERTER = {
    1: "DATA",
    2: "ACK",
    3: "NAK",
    4: "FIN",
}

class Package:
    type = 0  # diz se e pacote de dados ou de ack (preciso disso aqui?)
    seq_number = 0  # numero do pacote para ordenacao
    ack_number = 0  # o tcp tem isso entao vou colocar aqui
    window_size = 0  # tamanho da janela
    length = 0  # tamanho do pacote
    data = ""  # dados do pacote

    def __init__(self, type=0, seq_number=0, ack_number=0, window_size= 0, data="", bytes=None):
        if bytes:
            self.decode(bytes)
            return
        self.type = type
        self.seq_number = seq_number
        self.ack_number = ack_number
        self.window_size = window_size
        self.length = len(data)
        self.data = data

    def __str__(self):
        return (
            "Package(type={}, seq_number={}, ack_number={}, window_size={} length={}, data={})".format(
                TYPE_CONVERTER[self.type],
                self.seq_number,
                self.ack_number,
                self.window_size,
                self.length,
                self.data,
            )
        )

    def encode(self):
        if type(self.data) is str:
            self.data = self.data.encode()

        return (
            self.type.to_bytes(1, byteorder="big")
            + self.seq_number.to_bytes(4, byteorder="big")
            + self.ack_number.to_bytes(4, byteorder="big")
            + self.window_size.to_bytes(2, byteorder="big")
            + self.length.to_bytes(4, byteorder="big")
            + self.data
        )

    def decode(self, data):
        self.type = data[0]
        self.seq_number = int.from_bytes(data[1:5], byteorder="big")
        self.ack_number = int.from_bytes(data[5:9], byteorder="big")
        self.window_size = int.from_bytes(data[9:11], byteorder="big")
        self.length = int.from_bytes(data[11:15], byteorder="big")
        self.data = data[15 : self.length + 15].decode("utf-8")

    def checksum(self):
        return zlib.crc32(self.encode())
