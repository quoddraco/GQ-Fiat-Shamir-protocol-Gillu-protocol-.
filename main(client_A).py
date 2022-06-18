import socket
import random
import time

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "192.168.56.1"
PORT = 12334
connection.connect((IP, PORT))

def popi(data):# Функция раунла
    data=data.split(":")
##############################
    n=int(data[0])# Принятые данные от клиента В (сервера) (открытый ключ)
    e=int(data[1])#(открытый ключ)
    y=int(data[2])#(открытый ключ)
    x=int(data[3])#(секрет)
##############################
    print("n:",n)
    print("e:",e )
    print("y:",y )
    print("x:",x )

    r=random.randint(1,n-1)
    print("r:",r)

    a=pow(r,e,n)# a = r^e mod n
    print("a (r^e mod n):",a)

    mes=str(a)
    connection.send(mes.encode('utf-8'))# Отправляем (а) клиенту В
    while True:  # Слушаем клиента В
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    c=int(data)
    print("c:",c)

    z=(r*(x**c)) % n # z = r * x^c mod n
    print("z (r * x^c mod n):",z)

    mes=str(z)
    connection.send(mes.encode('utf-8'))# Отправляем (z) клиенту В

    while True:  # Слушаем клиента В
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    print("Исход проверки:",data)



# Начало программы
print("==========================")
atribut=random.randint(1,1000)
print("Атрибут:",atribut)
message="start"
connection.send(message.encode('utf-8'))# Отсылем клиенту В (серверу) о начале работы
time.sleep(2)
connection.send(str(atribut).encode('utf-8'))# Отсылем клиенту В (серверу) атрибут

while True:# Слушаем клиента В
    data = connection.recv(1024).decode('utf-8')
    if (data != ''):
        break

popi(data)# Запускаем функцию компонентов

print("==========================")

