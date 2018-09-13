# coding=utf-8
from __future__ import unicode_literals
from jolle import delete_database, create_database, transact, query
from jolle.shortcuts import (K, V, S, E, _, IN, D, GT, GTE, LT, LTE, NE, cmap,
                             FIND, WHERE, true, false)
from transit.transit_types import Keyword, Symbol

# Working with the datomic db.
###


def field(ident, db_type, doc, cardinality="one"):
    return {
        K.db.ident: Keyword(ident),
        Keyword("db/valueType"): Keyword("db.type/" + db_type),
        Keyword("db/cardinality"): Keyword("db.cardinality/" + cardinality),
        Keyword("db/doc"): doc,
    }


# yapf: disable
DB = "datomic:mem://t1"
print delete_database(DB)
print create_database(DB)

MOVIE_SCHEMA = [
    field("movie/title", "string", "The title of the movie"),
    field("movie/genre", "string", "The genre of the movie"),
    field("movie/release_year", "long",
          "The year the movie was released in theaters")]
print transact(DB, MOVIE_SCHEMA)

print transact(DB, [
    {
        K.movie.title: "The Goonies",
        K.movie.genre: "action/adventure",
        K.movie.release_year: 1985
    },
    cmap(prefix="movie", title="Commando", genre="action", release_year=1938),
    {
        Keyword("movie/title"): u"øptur",
        Keyword("movie/genre"): "punk dystopia",
        Keyword("movie/release_year"): 1984
    }
])
movies = query([
    K.find, [S.max, V.year],
    IN, D, V.released,
    K.where,
        [V.e, K.movie.title, V.title],
        [V.e, K.movie.release_year, V.year],
        [V.e, K.movie.genre, V.genre],
        #[V.e, K.movie.release_year, V.released],
        [(NE, V.year, 1985)]
], DB, 1938)
print movies
print "A"
for movie in movies:
    print u", ".join(unicode(x) for x in movie)
print "B"

# As a tree?
TREE_SCHEMA = [
    {
        K.db.index: true,
        K.db.ident: K.node.title,
        K.db.valueType: K.db.type.string,
        K.db.cardinality: K.db.cardinality.one,
        #K.db.unique: K.db.unique.identity
    },
    {
        K.db.index: true,
        K.db.ident: K.node.parent,
        K.db.valueType: K.db.type.ref,
        K.db.cardinality: K.db.cardinality.one,
        #K.db.unique: K.db.unique.identity
    }
]
print transact(DB, TREE_SCHEMA)
x = transact(DB, [
    {K.node.title: "Rod1", K.db.id: "i1"},
    {K.node.title: "Rod1", K.db.id: "i4"},
    {K.node.title: "Rod2", K.db.id: "i2"},
    {K.node.title: "Rod3", K.db.id: "i3"},
    {K.node.title: "Blad", K.node.parent: "i1"},
    {K.node.title: "Blad", K.node.parent: "i2"},
    {K.node.title: "Blad", K.node.parent: "i3"},
    {K.node.title: "Rod"},
    #{K.node.title: "Strammefa3a", K.db.id: "id"},
    #{K.node.title: "Grern1edf", K.node.parent: "id"},
])

# print query(
#     FIND, V.e, V.title, V.parent,
#     WHERE, []
# )
# assert False

print query([
    FIND, V.title, V.parent,
    WHERE,
        [V.e, K.node.title, V.title],
        [V.e, K.node.parent, V.parent]
], DB)



print "FOOOO"
for x in query([
    K.find, V.e, V.title, V.parent,
    K.where,
        [V.e, K.node.title, V.title],
        [[S.get_else, D, V.e, K.node.parent, "N/A"], V.parent]
], DB):
    print x

print "a"
for x in query([
    K.find, V.e, V.title, V.parent,
    IN, D, V("%"),
    K.where,
        [V.e, K.node.title, V.title],
        [[S.get_else, D, V.e, K.node.parent, "N/A"], V.parent]
], DB, [V.e, V.title, V.parent, {K.node.parent: 6}]):
    print x

#print query([FIND, V.name, WHERE, [V.e, K.node.title, V.name]], DB)

# yapf: enable
