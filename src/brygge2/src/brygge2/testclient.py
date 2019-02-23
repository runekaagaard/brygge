# coding=utf-8
import socket
from contextlib import closing

from transit.writer import Writer
from transit.reader import Reader
from transit.transit_types import Keyword

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


print write({Keyword("content"): [u'øæåØÆÅ', 2, 3, 4]})
