import socket
import random
from math import gcd as bltin_gcd

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = socket.gethostbyname(socket.gethostname())
PORT = 12334
listener.bind((IP, PORT))
listener.listen(0)
connection, address = listener.accept()


def coprime2(a, b):# Проверка на взаимно-простые числа
    return bltin_gcd(a, b) == 1

def fi(n):# функция эйлера
    f = n
    if n%2 == 0:
        while n%2 == 0:
            n = n // 2
        f = f // 2
    i = 3
    while i*i <= n:
        if n%i == 0:
            while n%i == 0:
                n = n // i
            f = f // i
            f = f * (i-1)
        i = i + 2
    if n > 1:
        f = f // n
        f = f * (n-1)
    return f


def proverka(n):# Функция разложения чисел на множители
    d=2
    a = []
    while d*d <= n:
        if n%d == 0:
            a.append(d)
            n //= d
        else:
            if d % 2 != 0:
                d += 2
            else:
                d+= 1
    if n>1:
        a.append(n)
    return a


def generate():
    while True:# Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break

    J=int(data)# атрибут клиента А

    print("Атрибут клиента A:",J)


    while True:  # Генерим простое число q
        q = random.randint(100, 999)
        a = proverka(q)
        if len(a) == 1:
            break
    while True:  # Генерим простое число p
        p = random.randint(100, 999)
        a = proverka(p)
        if len(a) == 1:
            break
    print("q (Простое число):", q)
    print("p (Простое число):", p)
    n = q * p
    print("n=(q*p):", n)

    f=fi(n)
    print("Число фукнции Эйлера Q(n):", f)

    while True:
         e=random.randint(1,f)
         if coprime2(e, f)==True:
              break

    print("Число е:", e)
    s = pow(e,-1,f)
    #s = (e**-1) % f
    print("Число s (e^-1 mod fi(n)):",s)

    x = pow(J,-s,n)
    print("Секрет x (J^-s mod n):",x)

    y = pow(x,e,n)
    print("Число y (x^e mod n):",y)

    print("Открытый ключ {n,e,y}:",n, e, y)

    message="{}:{}:{}:{}".format(n,e,y,x)
    connection.send(message.encode('utf-8'))  # Отсылаем сообщение клиенту А

    while True:# Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    a=int(data)
    print("a:",a)

    c=random.randint(0,e-1)
    mes=str(c)
    connection.send(mes.encode('utf-8'))  # Отсылаем сообщение клиенту А

    while True:# Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    z=int(data)
    print("z:",z)

    if (pow(z,e) %n==(a*(y**c)) % n): # Проверка!
           print("Исход проверки: Успех!")
           mes="Успех!"
           connection.send(mes.encode('utf-8'))  # Отсылаем сообщение клиенту А
    else:
        print("Исход проверки: False!")
        mes="False!"
        connection.send(mes.encode('utf-8'))  # Отсылаем сообщение клиенту А


def listen():
    while True:# Слушаем клиента А
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    print(data)
    if data=="start":
        generate()# запуск компонентов

print("==========================")
# Начало программы
listen()
print("==========================")