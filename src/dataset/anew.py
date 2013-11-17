# -*- coding: utf-8 -*-

from operator import itemgetter
from csv import DictReader

from fn import F

from . import load as _load

__all__ = ('iter_parse', 'load')


def _normalize_value(value):
    return float(value) / 4.0 - 1.25


def iter_parse(path):
    with open(path, 'r') as fin:
        rdr = DictReader(fin)
        for record in rdr:
            yield record


def load(path):
    value_getter = F(itemgetter('Valence Mean')) >> _normalize_value
    return _load(path, iter_parse, key=itemgetter('Description'), value=value_getter)
