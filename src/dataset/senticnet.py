#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter

from lxml.etree import parse as xmlparse

from . import load as _load

__all__ = ('iter_parse', 'load')


def _normalize_term(term):
    return term.replace(' ', '_').lower()


def iter_parse(path):
    root = xmlparse(path).getroot()
    nsmap = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'api': 'http://sentic.net/api/',
    }

    for concept in root.iterfind('.//rdf:Description', nsmap):
        text = concept.find('./api:text', nsmap).text
        polarity = concept.find('./api:polarity', nsmap).text
        yield {'text': _normalize_term(text), 'polarity': float(polarity)}


def load(path):
    return _load(path, iter_parse, key=itemgetter('text'), value=itemgetter('polarity'))
