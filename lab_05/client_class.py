import socket
import json
import time


file_to_send = '/Users/konstantinnistratov/PycharmProjects/interprocess_communication/lab_05/to_send/cat.jpeg'


class ClientSocket:
    def __init__(
            self,
            address_ip: str = 'localhost',
            port: int = 55005
    ):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((address_ip, port))

    def __del__(self):
        self.close_connection()

    def close_connection(self) -> None:
        self.__sock.close()

    def __send_data(self, data) -> None:
        self.__sock.send(data)

    def send_text(self, message: str) -> None:
        self.__send_data(self.dict_to_bytes({'type': 'text'}))
        time.sleep(1)
        print('Отправка текста')
        self.__send_data(self.dict_to_bytes({'data': message}))
        print('Текст успешно отправлен')

    def send_image_jpeg(self, image_path: str = file_to_send) -> None:
        self.__send_data(self.dict_to_bytes({'type': 'image/jpeg'}))
        file = open(image_path, "rb")
        print('Отправка пакетов')
        while True:
            file_data = file.read(4096)
            time.sleep(0.1)
            self.__send_data(file_data)
            print('.', end='')
            if not file_data:
                break
        print()
        print('Фотография успешно отправлена')
        file.close()

    @staticmethod
    def dict_to_bytes(to_send: dict) -> bytes:
        return json.dumps(to_send).encode()


if __name__ == '__main__':
    client = ClientSocket()
    client.send_text('Hello')
    # client.send_text('World')
