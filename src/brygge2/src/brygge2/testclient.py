# coding=utf-8
import socket
from contextlib import closing

from transit.writer import Writer
from transit.reader import Reader
from transit.transit_types import Keyword as K, Symbol as S, List as L

SERVER_ADDRESS = '/tmp/brygge.sock'
TRANSFER_PROTOCOL = "msgpack"


def write(data):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDRESS)
    with closing(sock):
        sockfile = sock.makefile('wrb')
        with closing(sockfile):
            Writer(sockfile, TRANSFER_PROTOCOL).write(data)
            return Reader(TRANSFER_PROTOCOL).read(sockfile)


print write(L([S('*'), 2, 2, 2, 2]))

# (require '[clojure.set :refer [difference]])
print write(
    L([
        S('require'),
        L([S('quote'), [S('clojure.set'),
                        K('refer'), [S('difference')]]])
    ]))

# (difference #{1 2 3} #{3 4 5 6})
print write(L([S('difference'), {1, 2, 3}, {3, 4, 5}]))
