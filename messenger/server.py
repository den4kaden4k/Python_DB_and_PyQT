from socket import socket, AF_INET, SOCK_STREAM
from select import select
from common.settings import MAX_CONNECTIONS, RESPONSE_409, RESPONSE_200, PRESENCE, MESSAGE, NAME, ADDRESS, ALL, \
    SERVER, TO, VALUE, ERROR, ACTION
from common.utils import get_time, parse_args, read_message, send_message
from common.decorators import log
from log.config_log_server import LOGGER


@log(LOGGER)
def join_user(data, user, user_list):
    if data[NAME] not in user_list:
        user_list[data[NAME]] = user
        log_message = f'{get_time()}: {data[ADDRESS]}: <{data[NAME]}> присоединился к чату'
        print(log_message)
        LOGGER.debug(log_message)
        send_message(RESPONSE_200, user)
        data.update(action=MESSAGE,
                    name=SERVER,
                    timestamp=get_time(),
                    value=f'{data[NAME]} присоединился к чату')
        return data
    send_message(RESPONSE_409, user)


@log(LOGGER)
def left_user(user, w_clients, user_list, clients):
    name = ''
    for key, value in user_list.items():
        if value == user:
            name = key
            break
    log_message = f'{get_time()}: Клиент {user.getpeername()} <{name}> отключился'
    print(log_message)
    LOGGER.debug(log_message)
    mes = dict(action=MESSAGE, to=ALL, name=SERVER, value=f'{name} покинул чат')
    try:
        user_list.pop(name)
    except KeyError:
        pass
    clients.remove(user)
    user.close()
    if w_clients and user_list:
        send_dest_mes(mes, w_clients, user_list)


def send_dest_mes(mes, w_clients, user_list, r_client=None):
    if mes[TO] == ALL:
        if len(w_clients) == 1 and mes[NAME] != SERVER:
            mes.update(to=list(user_list)[0], name=SERVER, value=f'В данный момент вы в чате один:(')
            send_message(mes, w_clients[0])
        else:
            for w_client in w_clients:
                if w_client != r_client and not w_client._closed:
                    send_message(mes, w_client)
    elif mes[TO] in user_list:
        send_message(mes, user_list[mes[TO]])
    else:
        mes.update(to=mes[NAME], name=SERVER, value=f'<{mes[TO]}> в данный момент недоступен')
        send_message(mes, r_client)


def message(data):
    print(f'{get_time()}: {data[ADDRESS]}: <{data[NAME]}>: {data[VALUE]}')
    return dict(to=data[TO],
                value=f'{get_time()}: {data[NAME]} to {data[TO]} >>> {data[VALUE]}')


def main():
    name_and_socket = {}
    clients = []
    address = parse_args()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(MAX_CONNECTIONS)
    sock.settimeout(0.2)
    mes = f'{get_time()}: [Server started]'
    print(mes)
    LOGGER.debug(mes)
    while True:
        try:
            client, addr = sock.accept()
            clients.append(client)
        except OSError:
            pass
        finally:
            r, w = [], []
            if clients:
                try:
                    r, w, e = select(clients, clients, [], 0)
                except Exception as e:
                    LOGGER.critical(e.__class__.__name__)
                for r_client in r:
                    request = read_message(r_client)
                    if ERROR in request.keys():
                        left_user(r_client, w, name_and_socket, clients)
                        continue
                    request[ADDRESS] = r_client.getpeername()
                    if request[ACTION] == PRESENCE:
                        response = join_user(request, r_client, name_and_socket)
                        if response:
                            send_dest_mes(response, w, name_and_socket, r_client)
                    elif request[ACTION] == MESSAGE:
                        send_dest_mes(request, w, name_and_socket, r_client)


if __name__ == '__main__':
    main()
