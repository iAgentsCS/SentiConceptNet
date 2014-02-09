# -*- coding: utf-8 -*-

from randwalk import random_walk

__all__ = ('calc_impacts',)


def calc_impacts(graph, alpha):
    n = graph.shape[0]
    certs = [0.0] * n
    for idx in xrange(n):
        certs[idx] = 1.0
        _, certs_out = random_walk(graph, certs, certs, alpha)
        certs[idx] = 0.0
        impact = sum(certs_out)
        print idx, impact
        yield impact
