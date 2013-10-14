#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt

from numpy.linalg import norm

__all__ = ('alignig_zero', 'unifying_dist')


def alignig_zero(values, seeds):
    for idx, value in enumerate(seeds):
        if value == 0.0:
            zero_idx = idx
            break

    zero = values[zero_idx]
    return [x - zero if x is not None else None for x in values]


def unifying_dist(values, seeds):
    idx_list = [idx for idx in xrange(len(seeds)) if seeds[idx] is not None]
    n = len(idx_list)

    muX = sum(seeds[idx] for idx in idx_list) / n
    varX = norm([(seeds[idx] - muX) for idx in idx_list])

    muY = sum(values[idx] for idx in idx_list) / n
    varY = norm([(values[idx] - muY) for idx in idx_list])

    p = sqrt(varX / varY)
    diff = muY * p - muX

    print diff
    return [y * p - diff if y is not None else None for y in values]
