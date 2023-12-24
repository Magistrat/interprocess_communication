import socket
import json

file_path = '/Users/konstantinnistratov/PycharmProjects/interprocess_communication/lab_04/received/'


sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
address = ('localhost', 55005)
print('Запуск сервера на {} порт {}'.format(*address))
sock.bind(address)
sock.listen(1)

while True:
    print('Ожидание соединения... Для закрытия нажать Ctr+C')
    client_socket, client_address = sock.accept()
    print(f'Подключено к {client_address}')
    try:
        header = client_socket.recv(1024)
        if header:
            header = json.loads(header)
            header_type = header.get('type')

            if header_type == 'text':
                message = client_socket.recv(1024)
                if message:
                    message = json.loads(message)
                    print('Передан текст:', message.get('data'))
            elif header_type == 'image/jpeg':
                file = open(file_path + '123.jpeg', "wb")
                while True:
                    file_data = client_socket.recv(4096)
                    file.write(file_data)
                    print('.', end='')
                    if not file_data:
                        break

    finally:
        print()
        print('Закрытие соединения')
        client_socket.close()
