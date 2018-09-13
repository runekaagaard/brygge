# coding=utf-8
from __future__ import unicode_literals
from transit.writer import Writer
from transit.reader import Reader
from requests import post
from StringIO import StringIO
from transit.transit_types import Keyword


class DatomicError(Exception):
    pass


def _request(action, datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write({Keyword("content"): datoms})
    r = post(
        "http://127.0.0.1:8080/" + action,
        data=io.getvalue().encode('utf-8'),
        headers={
            'Content-Type': "application/transit+json; charset=utf-8",
        })

    try:
        reader = Reader()
        data = reader.read(StringIO(r.content))
    except:
        print "ILLEGAL RESPONSE: "
        try:
            print r.content
        except UnboundLocalError:
            print "NO RESPONSE"
        pass
    if not r:
        raise DatomicError(data[Keyword("content")])
    else:
        return data[Keyword("content")]


def transact(*args):
    return _request("transact", args)


def query(*args, **kwargs):
    flat = kwargs.pop('flat', False)
    result = _request("query", args)
    if flat is True:
        return tuple([x[0] for x in result])
    else:
        return result


def create_database(db):
    return _request("create-database", db)


def delete_database(db):
    return _request("delete-database", db)
