"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
from subprocess import Popen, PIPE
import socket


def host_ping(pool_ip):
    for item in pool_ip:
        try:
            ip = socket.gethostbyname(item)
            proc = Popen(['ping', ip], stdout=PIPE)
            code = proc.wait()
            if code:
                print(f'{item} --> недоступен')
            else:
                print(f'{item} --> доступен')
        except socket.gaierror:
            print(f'{item} --> адрес или имя хоста некорректно')


hosts = ['google.com', '192.168.1111.1111', 'yandex.ru', '192.168.8.1']
host_ping(hosts)
