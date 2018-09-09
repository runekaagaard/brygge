from transit.writer import Writer
from transit.reader import Reader
from requests import post
from StringIO import StringIO
from transit.transit_types import Keyword as K, Symbol as S


def _request(action, datoms):
    io = StringIO()
    writer = Writer(io)
    writer.write({K("content"): datoms})
    try:
        r = post(
            "http://127.0.0.1:8080/" + action,
            data=io.getvalue(),
            headers={'Content-Type': "application/transit+json"})
        reader = Reader()
        data = reader.read(StringIO(r.text))
        return data[K("content")]
    except Exception as e:
        try:
            print r.text
        except UnboundLocalError:
            pass
        raise e


def transact(datoms):
    return _request("transact", datoms)


def query(datoms):
    return _request("query", datoms)


def field(ident, db_type, doc, cardinality="one"):
    return {
        K("db/ident"): K(ident),
        K("db/valueType"): K("db.type/" + db_type),
        K("db/cardinality"): K("db.cardinality/" + cardinality),
        K("db/doc"): doc,
    }


# yapf: disable
MOVIE_SCHEMA = [
    field("movie/title", "string", "The title of the movie"),
    field("movie/genre", "string", "The genre of the movie"),
    field("movie/release_year", "long",
          "The year the movie was released in theaters")]
print transact(MOVIE_SCHEMA)

print transact([{
        K("movie/title"): "The Goonies",
        K("movie/genre"): "action/adventure",
        K("movie/release_year"): 1985
    }, {
        K("movie/title"): "Commando",
        K("movie/genre"): "action/adventure",
        K("movie/release_year"): 1985
    }, {
        K("movie/title"): "Optur",
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
])
for movie in movies:
    print u", ".join(unicode(x) for x in movie)
# yapf: enable
