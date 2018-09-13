# coding=utf-8
from __future__ import unicode_literals
from transit.transit_types import Keyword, Symbol, true, false
from transit.pyversion import string_types


class KeywordUnicorn(Keyword):
    def __init__(self):
        self.parent = None

    def __getattr__(self, value):
        assert isinstance(value, string_types)
        if self.__dict__["parent"] is None:
            k = KeywordUnicorn()
            k.parent = k
            k.str = value
            k.hv = value.__hash__()
            return k
        else:
            self.str = self.str.replace("/", ".") + "/" + value
            self.hv = self.str.__hash__()
            return self

    def __call__(self, value):
        return Keyword(value)


class VariableUnicorn(object):
    def __getattr__(self, value):
        return Symbol("?" + value)

    def __call__(self, value):
        return Symbol("?" + value)


class SymbolUnicorn(object):
    def __getattr__(self, value):
        return Symbol(value.replace("_", "-"))

    def __call__(self, value):
        return Symbol(value.replace("_", "-"))


def cmap(**kwargs):
    prefix = kwargs.pop("prefix", None)
    maybe_prefix = (lambda x: x) if prefix is None else (
        lambda x: prefix + "/" + x)

    return {Keyword(maybe_prefix(k)): v for k, v in kwargs.iteritems()}


K = KeywordUnicorn()
S = SymbolUnicorn()
V = VariableUnicorn()

E = Symbol("?e")
_ = Symbol("_")
FIND = Keyword("find")
WHERE = Keyword("where")
IN = Keyword("in")
D = Symbol("$")
GT = Symbol(">")
GTE = Symbol(">=")
LT = Symbol("<")
LTE = Symbol("<=")
NE = Symbol("!=")
