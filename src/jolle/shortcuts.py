# coding=utf-8
from __future__ import unicode_literals
from transit.transit_types import Keyword, Symbol
from transit.pyversion import string_types


class KeywordUnicorn(Keyword):
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


class VariableUnicorn(object):
    def __getattr__(self, value):
        return Symbol("?" + value)


class SymbolUnicorn(object):
    def __getattr__(self, value):
        return Symbol(value)


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
IN = Keyword("in")
D = Symbol("$")
GT = Symbol(">")
GTE = Symbol(">=")
LT = Symbol("<")
LTE = Symbol("<=")
NE = Symbol("!=")
