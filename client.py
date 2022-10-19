import socket
import re

sock = socket.socket()

try:
    port = int(input('Введите номер порта, к которому хотите подключиться (от 1024 до 65535) '))
    if port < 1023 or port > 65535:
        port = 9090
        print('Обнаружено число вне допустимых границ')
        print('Присвоено значение по умолчанию - 9090')
except ValueError:
    print('Обнаружен не числовой тип данных')
    port = 9090
    print('Присвоено значение по умолчанию - 9090')
print('Присвоено значение - ' + str(port))

host = input('Введите адрес хоста, к которому хотите подключиться в формате 0.0.0.0 ')
if re.fullmatch(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host):
    print('Задан адрес хоста - ' + host)
else:
    print('Обнаружен неверный ввод')
    host = '127.0.0.1'
    print('Было присвоено значение по умолчанию - 127.0.0.1')

sock.connect((host, port))
print('Вы подключились к серверу 127.0.0.1')

print('Аутентификация')
message1 = sock.recv(1024)
print(message1.decode())

password = input()
sock.send(password.encode())

message2 = sock.recv(1024)
while message2.decode() == 'Неверный пароль':
    print(message2.decode())
    password = input('Введите пароль ')
    sock.send(password.encode())
    message2 = sock.recv(1024)

while True:
    msg = input('Введите данные, которые хотите отправить на сервер ')
    if msg == 'exit':
        sock.send(msg.encode())
        sock.close()
        print('Соединение с сервером разорвано')
        break

    else:
        sock.send(msg.encode())
        print('Данные отправлены на сервер')

        data = sock.recv(1024)

        print('Сообщение, полученное от сервера - ' + data.decode())