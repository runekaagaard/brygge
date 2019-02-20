# coding=utf-8
import socket
import sys
from transit.writer import Writer
from transit.reader import Reader
from StringIO import StringIO
from transit.transit_types import Keyword


class UDSIO(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sio = StringIO()
        server_address = '/tmp/foo'
        print >> sys.stderr, 'connecting to %s' % server_address
        try:
            self.sock.connect(server_address)
        except socket.error, msg:
            print >> sys.stderr, msg
            sys.exit(1)

    def flush(self):
        pass

    def write(self, msg):
        self.sock.send(msg)

    def recv(self):
        try:
            amount_received = 0
            amount_expected = 17

            while amount_received < amount_expected:
                data = self.sock.recv(16)
                amount_received += len(data)
                print >> sys.stderr, 'received "%s"' % data

        finally:
            print >> sys.stderr, 'closing socket'
            self.sock.close()


io = UDSIO()
writer = Writer(io)
writer.write({Keyword("content"): [1, 2, 3, 4]})
io.recv()
