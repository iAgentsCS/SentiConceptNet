# -*- coding: utf-8 -*-

from itertools import ifilter, imap, izip

from numpy import loadtxt, copy
from numpy.linalg import norm
from scipy.sparse import coo_matrix
from sklearn.preprocessing import normalize

__all__ = ('load_graph', 'random_walk')


def _normalize(graph, axis):
    return normalize(graph + graph.T, norm='l1', axis=axis, copy=False)


def load_graph(path, axis, f=None):
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
        indices['weight'].append(1.0)

        indices['start'].append(row['end'])
        indices['end'].append(row['start'])
        indices['weight'].append(1.0)

        N = max(N, row['start'], row['end'])

    N += 1
    graph = []
    for indices in indices_list:
        m = coo_matrix((indices['weight'],
                       (indices['start'], indices['end'])),
                       shape=(N, N))
        graph.append(m)

    graph = sum(imap(coo_matrix.tocsr, graph))
    return _normalize(graph, axis)


def random_walk(graph, values, certs, alpha):
    init = copy(values)
    cert_init = copy(certs)

    diff = float('infinity')
    while diff > 0.001:
        prev = copy(values)
        values = (1 - alpha) * graph * values + alpha * init
        certs = (1 - alpha) * graph * certs + alpha * cert_init

        diff = norm(values - prev)
        #print 'diff = ' + str(diff)

    values = [v if c > 0.0 else None for v, c in izip(values, certs)]
    return values, certs
