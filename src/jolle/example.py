# coding=utf-8
from __future__ import unicode_literals
from jolle import create_database, transact, query
from jolle.shortcuts import (K, V, S, E, _, IN, D, GT, GTE, LT, LTE, NE, cmap)
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
    {K.db.ident: K.tree.node.title,
     K.db.valueType: K("db.type/string"),
     K.db.cardinality: K("db.cardinality/one"),
     K.db.unique: K("db.unique/identity")},
    {K.db.ident: K.tree.node.parent,
     K.db.valueType: K("db.type/ref"),
     K.db.cardinality: K("db.cardinality/many"),
     K.db.unique: K("db.unique/identity")},
]
print transact(DB, TREE_SCHEMA)
from uuid import uuid4
u = str(uuid4)
x = transact(DB, [
    {K.tree.node.title: "Stammea3a", K.db.id: u},
    {K.tree.node.title: "Gren1edf", K.tree.node.parent: u},
])
print x

# yapf: enable
