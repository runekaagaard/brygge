# coding=utf-8
from __future__ import unicode_literals
from transit.writer import Writer
from transit.reader import Reader
from requests import post
from StringIO import StringIO
from transit.transit_types import Keyword as K, Symbol as S


class DatomicError(Exception):
    pass


def _request(action, datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write({K("content"): datoms})
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
        raise DatomicError(data[K("content")])
    else:
        return data[K("content")]


def transact(*args):
    return _request("transact", args)


def query(*args):
    return _request("query", args)


def create_database(db):
    return _request("create-database", db)


def field(ident, db_type, doc, cardinality="one"):
    return {
        K("db/ident"): K(ident),
        K("db/valueType"): K("db.type/" + db_type),
        K("db/cardinality"): K("db.cardinality/" + cardinality),
        K("db/doc"): doc,
    }


# yapf: disable
DB = "datomic:mem://t1"
print create_database(DB)

MOVIE_SCHEMA = [
    field("movie/title", "string", "The title of the movie"),
    field("movie/genre", "string", "The genre of the movie"),
    field("movie/release_year", "long",
          "The year the movie was released in theaters")]
print transact(DB, MOVIE_SCHEMA)

print transact(DB, [{
        K("movie/title"): "The Goonies",
        K("movie/genre"): "action/adventure",
        K("movie/release_year"): 1985
    }, {
        K("movie/title"): "Commando",
        K("movie/genre"): "action/adventure",
        K("movie/release_year"): 1985
    }, {
        K("movie/title"): u"øptur",
        K("movie/genre"): "punk dystopia",
        K("movie/release_year"): 1984
    }
])
movies = query([
    K("find"), S("?title"), S("?genre"), S("?year"),
    K("where"),
        [S("?e"), K("movie/title"), S("?title")],
        [S("?e"), K("movie/release_year"), S("?year")],
        [S("?e"), K("movie/genre"), S("?genre")],
], DB)
print "A"
for movie in movies:
    print u", ".join(unicode(x) for x in movie)
print "B"
# yapf: enable
