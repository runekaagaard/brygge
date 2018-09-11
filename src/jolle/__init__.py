# coding=utf-8
from __future__ import unicode_literals
from transit.writer import Writer
from transit.reader import Reader
from requests import post
from StringIO import StringIO
from transit.transit_types import Keyword as K, Symbol as S
from transit.pyversion import string_types


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


"""TESTING"""

# Different kind of magic.
###


def field(ident, db_type, doc, cardinality="one"):
    return {
        k.db.ident: K(ident),
        K("db/valueType"): K("db.type/" + db_type),
        K("db/cardinality"): K("db.cardinality/" + cardinality),
        K("db/doc"): doc,
    }


class KeywordUnicorn(K):
    def __init__(self):
        self.parent = None

    def __getattr__(self, value):
        assert isinstance(value, string_types)
        if self.__dict__["parent"] is None:
            instance = KeywordUnicorn()
            instance.parent = instance
            instance.str = value
            instance.hv = value.__hash__()
            return instance
        else:
            self.str += u"/" + value
            self.hv = self.str.__hash__()
            return self


class SymbolUnicorn(object):
    def __getattr__(self, value):
        return S("?" + value)


def cmap(**kwargs):
    prefix = kwargs.pop("prefix", None)
    maybe_prefix = (lambda x: x) if prefix is None else (
        lambda x: prefix + "/" + x)

    return {K(maybe_prefix(k)): v for k, v in kwargs.iteritems()}


k = KeywordUnicorn()
s = SymbolUnicorn()

E = S("?e")
_ = S("_")
IN = K("in")
FIND = K("find")
WHERE = K("where")
D = S("$")

# Working with the datomic db.
###

# yapf: disable
DB = "datomic:mem://t1"
print create_database(DB)

MOVIE_SCHEMA = [
    field("movie/title", "string", "The title of the movie"),
    field("movie/genre", "string", "The genre of the movie"),
    field("movie/release_year", "long",
          "The year the movie was released in theaters")]
print transact(DB, MOVIE_SCHEMA)

print transact(DB, [
    {
        k.movie.title: "The Goonies",
        k.movie.genre: "action/adventure",
        k.movie.release_year: 1985
    },
    cmap(prefix="movie", title="Commando", genre="action", release_year=1938),
    {
        K("movie/title"): u"øptur",
        K("movie/genre"): "punk dystopia",
        K("movie/release_year"): 1984
    }
])
movies = query([
    FIND, s.title, s.genre, s.year,
    IN, D, s.released,
    WHERE,
        [E, k.movie.title, s.title],
        [E, k.movie.release_year, s.year],
        [E, k.movie.genre, s.genre],
        [E, k.movie.release_year, s.released],
], DB, 1938)
print movies
print "A"
for movie in movies:
    print u", ".join(unicode(x) for x in movie)
print "B"
# yapf: enable
