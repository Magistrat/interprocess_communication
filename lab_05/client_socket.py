import socket
import json
from typing import Tuple, Dict
import time

file_to_send = '/Users/konstantinnistratov/PycharmProjects/interprocess_communication/lab_05/to_send/cat.jpeg'


def dict_to_bytes(to_send: dict):
    return json.dumps(to_send).encode()


def main(
        server_address: Tuple[str, int],
        header: Dict[str, str],
        message: Dict[str, str]
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    sock.send(dict_to_bytes(header))
    time.sleep(1)

    header_type = header.get('type')
    if header_type == 'text':
        sock.send(dict_to_bytes(message))
    elif header_type == 'image/jpeg':
        filename = message.get('data')
        file = open(filename, "rb")

        while True:
            file_data = file.read(4096)
            time.sleep(0.1)
            sock.send(file_data)
            print('.', end='')
            if not file_data:
                break
    else:
        raise ValueError(f'Неизвестный тип для передачи: {header_type}')

    sock.close()


if __name__ == '__main__':
    address = ('localhost', 55005)

    header_data = {
        # 'type': 'text',
        'type': 'image/jpeg'
    }
    message_data = {
        # 'data': 'Hello World',
        'data': file_to_send
    }

    main(
        server_address=address,
        header=header_data,
        message=message_data
    )
