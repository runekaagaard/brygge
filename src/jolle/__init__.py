from transit.writer import Writer
from requests import post
from StringIO import StringIO
from transit.transit_types import Keyword as K, Symbol as S


def transact(datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write(datoms)
    r = post("http://127.0.0.1:8080/transact", data=io.getvalue())
    print r.text


def query(datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write(datoms)
    r = post("http://127.0.0.1:8080/query", data=io.getvalue())
    print r.text


transact([{K("foo"): "bar"}])
query([
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
"""
[:find ?title ?year ?genre 
 :where [?e :movie/title ?title] 
        [?e :movie/release-year ?year] 
        [?e :movie/genre ?genre]]
"""
