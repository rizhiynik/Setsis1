import socket

log_file = open('log_file.txt', 'a')

log_file.write('Сервер запущен\n')

users = {}

sock = socket.socket()

try:
	port = int(input('Введите номер порта, который будет использоваться сервером (от 1024 до 65535) '))
	if port < 1023 or port > 65535:
		port = 9090
		print('Обнаружено число вне допустимых границ')
		print('Порту было присвоено значение по умолчанию - 9090')
except ValueError:
	print('Обнаружен не числовой тип данных')
	port = 9090
	print('Порту было присвоено значение по умолчанию - 9090')
log_file.write('Порту присвоено значение - ' + str(port) + '\n')

sock.bind(('', port))
sock.listen(0)
log_file.write('Порт прослушивается\n')

while True:
	conn, addr = sock.accept()
	hostname = socket.gethostname()
	ip_address = socket.gethostbyname(hostname)

	check = 1
	if ip_address in users:
		try:
			log_file.write('Запрос у пользователя ' + ip_address + ' пароля')
		except ValueError:
			log_file = open('log_file.txt', 'a')
		conn.send('Введите пароль'.encode())
		user_password = conn.recv(1024)
		while user_password != users[ip_address]:
			conn.send('Неверный пароль'.encode())
			log_file.write('Клиент не прошел аутентификацию\n')
			user_password = conn.recv(1024)
		if user_password == users[ip_address]:
			conn.send('Добро пожаловать '.encode() + ip_address.encode())
			log_file.write('Клиент прошел аутентификацию\n')
		else:
			conn.send('Неверный пароль'.encode())
			log_file.write('Клиент не прошел аутентификацию\n')
			conn.close()
	else:
		log_file.write('Добавление нового клиента в базу сервера\n')
		conn.send('Введите новый пароль'.encode())
		user_password = conn.recv(1024)
		users[ip_address] = user_password
		conn.send('Добро пожаловать '.encode() + ip_address.encode())
		log_file.write('Клиент прошел аутентификацию\n')
	log_file.write('Подключился клиент ' + ip_address + '\n')

	while True:
		msg = ''
		log_file.write('Запрос данных от клиента\n')
		data = conn.recv(1024)
		if data.decode() == 'exit':
			log_file.write('Клиент разорвал соединение\n')
			conn.close()
			log_file.close()
			break
		else:
			if not data:
				break
			msg += data.decode()
			log_file.write('Отправка данных клиенту\n')
			conn.send(data + ' '.encode() + str(addr[1]).encode())

			log_file.write('Сообщение, полученное от клиента - ' + msg + '\n')

