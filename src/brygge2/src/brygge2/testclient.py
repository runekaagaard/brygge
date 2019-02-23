# coding=utf-8
import socket
import sys
from contextlib import closing
from StringIO import StringIO

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
            writer = Writer(sockfile, TRANSFER_PROTOCOL)
            writer.write(data)
            reader = Reader(TRANSFER_PROTOCOL)

            return reader.read(sockfile)


print write({Keyword("content"): [1, 2, 3, 4]})
