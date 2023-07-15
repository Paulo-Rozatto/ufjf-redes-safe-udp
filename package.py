# syn e fin foram geradas pelo copilot, sei la oq e isso
TYPE = {
    "DATA": 1,
    "ACK": 2,
    # "SYN": 3,
    # "FIN": 4,
}

TYPE_CONVERTER = {
    1: "DATA",
    2: "ACK",
    # 3: "SYN",
    # 4: "FIN",
}


class Package:
    type = 0
    number = 0
    length = 0
    data = ""

    def __init__(self, type=0, number=0, length=0, data="", bytes=None):
        if bytes:
            self.decode(bytes)
            return
        self.type = type
        self.number = number
        self.length = length
        self.data = data

    def __str__(self):
        return "Package(type={}, number={}, length={}, data={})".format(
            self.type, self.number, self.length, self.data
        )

    def encode(self):
        return (
            self.type.to_bytes(1, byteorder="big")
            + self.number.to_bytes(4, byteorder="big")
            + self.length.to_bytes(4, byteorder="big")
            + str.encode(self.data)
        )

    def decode(self, data):
        self.type = TYPE_CONVERTER[data[0]]
        self.number = int.from_bytes(data[1:5], byteorder="big")
        self.length = int.from_bytes(data[5:9], byteorder="big")
        self.data = data[9:].decode("utf-8")
