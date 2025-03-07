import socket
from time import sleep


class Client(socket.socket):
    """
        .
    """
    
    def __send_request(self):
        """
            .
        """
        pass

    def request_update_entry(self):
        """
            .
        """
        pass

    def request_query_all_users(self):
        """
            .
        """
        pass

    def request_query_users(self):
        """
            .
        """
        pass

    def request_query_all_rooms(self):
        """
            .
        """
        pass

    def request_query_rooms(self):
        """
            .
        """
        pass

    def request_query_all_hardware(self):
        pass
        """
            .
        """

    def request_query_hardware(self):
        """
            .
        """
        pass


    def __init__(self):
        super().__init__()
        connection:socket.socket = socket.create_connection(('192.168.178.30', 3000))
        try:
            data = 2
            connection.sendall(data.to_bytes(1, 'little'))
            data = 5
            for i in range(0, 1050):
                connection.sendall(data.to_bytes(1, 'little'))
            sleep(3)
        except Exception as e:
            print(f"Exception:{e}")
        except KeyboardInterrupt:
            pass
        finally:
            connection.close()


if __name__ == '__main__':
    Client()