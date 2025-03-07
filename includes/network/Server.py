import socket


class Server(socket.socket):
    """
        .
    """

    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.address = '192.168.178.30'
        print(f"""opening server on address:"{self.address}" and port 3000""")
        self.bind((self.address, 3000))
        self.listen(1)
        print('started listening')
        connection:socket = self.accept()[0]
        while True:
            data:bytes = connection.recv(32)
            if data:
                print('received:{}'.format(data))
            else:
                break

if __name__ == '__main__':
    Server()