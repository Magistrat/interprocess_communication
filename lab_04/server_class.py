import socket
import json

file_path = '/Users/konstantinnistratov/PycharmProjects/interprocess_communication/lab_04/received/'


class ServerSocket:
    def __init__(
            self,
            address_ip: str = 'localhost',
            port: int = 55005
    ):
        self.__client_socket = None
        self.client_address = None
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((address_ip, port))
        print(f'Запуск сервера на {address_ip} порт {port}')
        self.__sock.listen(1)
        self.infinity()

    def __del__(self):
        self.close_client()
        self.close_server()

    def close_client(self) -> None:
        if self.__client_socket:
            self.__client_socket.close()

    def close_server(self) -> None:
        self.__sock.close()

    def infinity(self):
        while True:
            print('Ожидание соединения... Для закрытия нажать Ctr+C')
            self.__client_socket, self.client_address = self.__sock.accept()
            print(f'Подключено к {self.client_address}')

            try:
                header = self.__client_socket.recv(1024)
                if header:
                    header = json.loads(header)
                    header_type = header.get('type')

                    if header_type == 'text':
                        print(self.get_message())
                    elif header_type == 'image/jpeg':
                        self.save_image_jpeg()
            finally:
                self.__client_socket.close()

    def get_message(self) -> str:
        message = self.__client_socket.recv(1024)
        if message:
            message = json.loads(message)
            return message.get('data')

    def save_image_jpeg(self):
        file = open(file_path + '123.jpeg', "wb")
        print('Получение пакетов')
        while True:
            file_data = self.__client_socket.recv(4096)
            file.write(file_data)
            print('.', end='')
            if not file_data:
                break
        print()
        print('Все пакеты получены')
        file.close()


if __name__ == '__main__':
    ServerSocket()
