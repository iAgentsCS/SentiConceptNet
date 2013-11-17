# -*- coding: utf-8 -*-

from collections import Counter, namedtuple
from csv import DictReader
from itertools import chain, imap, ifilter, starmap
from operator import attrgetter

from fn import F

__all__ = (
    'count',
    'iter_parse',
    'iter_edges',
    'iter_nodes',
    'iter_rels',
    'iter_filter_with_count',
    'simplify_edges',
    'wrap_edge'
)

_Count = namedtuple('Count', ('text', 'count'))
_Edge = namedtuple('Edge', ('rel', 'start', 'end', 'weight'))


def _accumulate(counter, edge):
    uri = edge['uri']
    weight = edge['weight']
    try:
        record = counter[uri]
        record['weight'] += float(weight)
        record['count'] += 1
    except KeyError:
        counter[uri] = {
            'rel': edge['rel'],
            'start': edge['start'],
            'end': edge['end'],
            'weight': float(weight),
            'count': 1
        }

    return counter


def _count(edges, counter=None):
    if counter is None:
        counter = {}

    return reduce(_accumulate, edges, counter)


def iter_parse(path):
    with open(path, 'r') as fin:
        rdr = DictReader(fin, delimiter='\t')
        for record in rdr:
            yield record


def iter_edges(paths, normalize=None, prefilter=None, postfilter=None):
    parse = F(imap, iter_parse) >> chain.from_iterable >> F(ifilter, prefilter)
    edges = parse(paths)

    counter = _count(edges)
    extract = F(imap, normalize) >> F(ifilter, postfilter)
    return extract(counter.itervalues())


def iter_nodes(edges):
    for edge in edges:
        yield edge['start']
        yield edge['end']


def iter_rels(edges):
    for edge in edges:
        yield edge['rel']


def iter_filter_with_count(count_filter, items):
    counter = Counter(items)
    extract = F(starmap, _Count) \
        >> F(ifilter, count_filter) \
        >> F(imap, attrgetter('text'))
    return extract(counter.iteritems())


def simplify_edges(edges, nodes, rels):
    nodes_idx = dict((c, i) for i, c in enumerate(nodes))
    rel_idx = dict((r, i) for i, r in enumerate(rels))

    result = []
    for edge in edges:
        try:
            rel = rel_idx[edge['rel']]
            start = nodes_idx[edge['start']]
            end = nodes_idx[edge['end']]
            weight = edge['weight']
            result.append(_Edge(rel, start, end, weight))
        except KeyError:
            pass

    return result


def wrap_edge(rel, start, end, weight):
    return _Edge(int(rel), int(start), int(end), float(weight))
