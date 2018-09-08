from transit.writer import Writer
from transit.reader import Reader
from requests import post
from StringIO import StringIO
from transit.transit_types import Keyword as K, Symbol as S


def transact(datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write(datoms)
    r = post(
        "http://127.0.0.1:8080/transact",
        data=io.getvalue(),
        headers={'Content-Type': "application/transit+json"})
    reader = Reader()
    return reader.read(StringIO(r.text))


def query(datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write(datoms)
    r = post("http://127.0.0.1:8080/query", data=io.getvalue())
    reader = Reader()
    return reader.read(StringIO(r.text))


print transact([{K("movie/title"): "bars1@foo.com"}])
print query([
    K("find"),
    S("?email"),
    K("where"), [S("?e"), K("person/email"),
                 S("?email")]
])
print query([
    K("find"),
    S("?title"),
    S("?year"),
    S("?genre"),
    K("where"), [S("?e"), K("movie/title"),
                 S("?title")], [S("?e"),
                                K("movie/release-year"),
                                S("?year")],
    [S("?e"), K("movie/genre"), S("?genre")]
])
