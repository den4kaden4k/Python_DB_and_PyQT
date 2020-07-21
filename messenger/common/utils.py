import argparse
import json
from datetime import datetime
import time
from json import JSONDecodeError

from common.settings import DEFAULT_IP, DEFAULT_PORT, MAX_PACKAGE, ENCODING, ERROR, RESPONSE_400


def get_date_time():
    return str(datetime.now())


def get_time():
    return time.strftime('%X')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP)
    parser.add_argument('-p', default=DEFAULT_PORT)
    args = parser.parse_args()
    return args.a, args.p


def read_message(socket):
    try:
        msg = json.loads(socket.recv(MAX_PACKAGE).decode(ENCODING))
        return msg
    except (ConnectionResetError, ConnectionRefusedError) as e:
        return {ERROR: e.__class__.__name__}
    except JSONDecodeError:
        return RESPONSE_400


def send_message(message, socket):
    try:
        socket.send(json.dumps(message).encode(ENCODING))
    except (ConnectionResetError, ConnectionRefusedError) as e:
        return {ERROR: e.__class__.__name__}
