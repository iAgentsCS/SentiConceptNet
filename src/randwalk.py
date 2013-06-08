#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import ifilter, imap
from math import sqrt

from numpy import loadtxt, copy
from numpy.linalg import norm
from scipy.sparse import coo_matrix
from sklearn.preprocessing import normalize

__all__ = ('load_graph', 'random_walk')


def _normalize(graph, axis):
    return normalize(graph + graph.T, norm='l1', axis=axis, copy=False)


def load_graph(path, f=None):
    dtype = {
        'formats': ('i', 'i', 'i', 'f8'),
        'names': ('rel', 'start', 'end', 'weight')}
    data = loadtxt(path, dtype=dtype, ndmin=1)

    N = 0
    R = max(data['rel']) + 1

    indices_list = [{'start': [], 'end': [], 'weight': []} for _ in xrange(R)]
    for row in ifilter(f, data):
        indices = indices_list[row['rel']]
        indices['start'].append(row['start'])
        indices['end'].append(row['end'])
        #indices['weight'].append(row['weight'])
        indices['weight'].append(1.0)
        N = max(N, row['start'], row['end'])

    N += 1
    graph = []
    for indices in indices_list:
        m = coo_matrix((indices['weight'], (indices['start'], indices['end'])), shape=(N, N))
        graph.append(m)

    return graph


def _alignig_zero(values, seeds):
    zero = values[810]
    return [x - zero for x in values]


def _unifying_dist(values, seeds):
    n = 919

    muX = sum(seeds) / n
    varX = norm([(x - muX) for x in seeds])

    sentiments = values[:n]
    muY = sum(sentiments) / n
    varY = norm([(y - muY) for y in sentiments])

    p = sqrt(varX / varY)
    diff = muY * p - muX

    print diff
    return [y * p - diff for y in values]


def random_walk(graph, values, alpha, axis):
    graph = sum(imap(coo_matrix.tocsr, graph))
    graph = _normalize(graph, axis)
    init = copy(values)

    diff = float('infinity')
    while diff > 0.001:
        prev = copy(values)
        values = (1 - alpha) * graph * values + alpha * init

        diff = norm(values - prev)
        print 'diff = ' + str(diff)

    return values
