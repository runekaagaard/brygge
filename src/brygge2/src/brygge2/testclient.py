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


#io = UDSIO()
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/brygge.sock'
sock.connect(server_address)

sock_out = sock.makefile('wb')
sock_in = sock.makefile('r')
sock.close()

writer = Writer(sock_out)
writer.write({Keyword("content"): [1, 2, 3, 4]})
print >> sock_out, ""
sock_out.close()
#io.recv()

print "------------"
print dir(sock_in), sock_in, type(sock_in)

#reader = Reader()
#reader.read(sock_in)
#for x in reader.readeach(sock_in):
#    print x
#sock_in.flush(b)
#print sock_in.read(200)
for line in sock_in:  # Python 2.2 only; 'in sockin.xreadlines(  )' in 2.1
    print 'received:', line,
