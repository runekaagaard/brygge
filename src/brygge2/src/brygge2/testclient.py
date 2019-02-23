# coding=utf-8
import socket
import sys
from contextlib import closing
from transit.writer import Writer
from transit.reader import Reader
from StringIO import StringIO
from transit.transit_types import Keyword

SERVER_ADDRESS = '/tmp/brygge.sock'


def write(data):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDRESS)
    with closing(sock):
        sockfile = sock.makefile('wrb')
        with closing(sockfile):
            writer = Writer(sockfile)
            writer.write(data)
            reader = Reader()

            return reader.read(sockfile)


print write({Keyword("content"): [1, 2, 3, 4]})
