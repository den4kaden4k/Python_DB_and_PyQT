from socket import socket, AF_INET, SOCK_STREAM
import time
from threading import Thread
from common.settings import DEFAULT_IP, DEFAULT_PORT, MAX_TRYING, RESPONSE, ERROR, PRESENCE, ALL, MESSAGE, EXIT, ACTION, \
    NAME, TO, VALUE, SERVICE, HELP
from common.utils import get_date_time, send_message, read_message, get_time
from common.decorators import log
from log.config_log_client import LOGGER


def presence(_name):
    return dict(action=PRESENCE, timestamp=get_date_time(), to=ALL, name=_name)


def message(source, dest, mes):
    return dict(action=MESSAGE, timestamp=get_date_time(), to=dest, name=source, value=mes)


def logout():
    return dict(action=EXIT, timestamp=get_date_time())


def user_interactive(sock, name):
    while True:
        try:
            command = input('Введите команду: (help - доступные команды) ')
            if command == MESSAGE:
                destination = input('Введите получателя (всем - отправить всем): ')
                input_msg = input('Введите сообщение: ')
                if input_msg.split() and destination.split():
                    mes = message(name, destination, input_msg)
                    send_message(mes, sock)
            elif command == EXIT:
                break
            elif command == HELP:
                show_help()
        except Exception as e:
            LOGGER.error(e.__class__.__name__)
            break


def show_help():
    print('Message - отправка сообщения\nExit - выход из программы\nHelp - помощь по командам')


def process_message(sock):
    while True:
        mes = read_message(sock)
        if mes:
            if ERROR in mes.keys():
                connection_error(mes[ERROR])
                break
            else:
                if mes[ACTION] == MESSAGE:
                    print(f'\n{get_time()}: От {mes[NAME]} Кому: {mes[TO]} >>> {mes[VALUE]}')
                elif mes[ACTION] == SERVICE:
                    print(mes[MESSAGE])


def connection_error(error):
    log_message = f'\n{get_date_time()}: Сервер недоступен. Нажмите Enter для выхода.'
    print(log_message)
    LOGGER.critical(error)


@log(LOGGER)
def try_connect():
    address = (DEFAULT_IP, DEFAULT_PORT)
    s = socket(AF_INET, SOCK_STREAM)
    count = 0
    while count < MAX_TRYING:
        try:
            s.connect(address)
            mes = f'Установлено соединение с сервером {address}'
            print(mes)
            LOGGER.debug(mes)
            return s
        except (ConnectionRefusedError, ConnectionResetError):
            count += 1
            if count == 1:
                print('Сервер недоступен')
            time.sleep(1)
            print(f'Повторное подключение... (осталось {MAX_TRYING - count} попыток)')

            continue
    s.close()
    return 0


def connect_server():
    while True:
        sock = try_connect()
        if not sock:
            next_step = input('Не удалось подключиться к серверу. Повторить попытку? '
                              '(да - повторить, нет - выйти из программы)\n')
            if next_step == 'да':
                continue
            else:
                LOGGER.debug('Выход из программы после неудачного соединения с сервером')
                return 0
        return sock


def user_registration(sock):
    while True:
        name = input('Введи свое имя: ')
        if not name.split():
            print('Имя не может быть не заполненым!')
            continue
        check_online = send_message(presence(name), sock)
        if not check_online:
            return name
        else:
            connection_error(check_online[ERROR])
            return 0


def main():
    _name = ''
    while True:
        sock = connect_server()
        if not sock:
            exit(1)
        _name = user_registration(sock)
        if _name:
            break

    while True:
        answer = read_message(sock)
        if answer and ERROR in answer.keys():
            connection_error(answer[ERROR])
            connect_server()
        elif answer and answer[ACTION] == PRESENCE and answer[RESPONSE] == 409:
            print(answer[ERROR])
            user_registration(sock)
        elif answer and answer[ACTION] == PRESENCE and answer[RESPONSE] == 200:
            break

    tr1 = Thread(target=process_message, args=(sock,))
    tr1.daemon = True
    tr1.start()
    tr2 = Thread(target=user_interactive, args=(sock, _name))
    tr2.daemon = True
    tr2.start()
    while tr1.is_alive() and tr2.is_alive():
        time.sleep(1)
    print('Выходим из программы...')
    time.sleep(3)
    sock.close()
    exit(1)


if __name__ == '__main__':
    main()
