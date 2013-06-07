#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import imap

from fn import F
from fn.op import flip

from dataset import (
    atof,
    anew,
    senticnet as sn,
    conceptnet as cn,
    filters
)
from iterreg import iterreg
from eval import polarity_accuracy, kendall_tau

__all__ = (
    'handle_split',
    'handle_seed',
    'handle_iterreg',
    'handle_eval'
)


def _save(path, lines):
    lines = imap('{0}\n'.format, lines)
    with open(path, 'w') as fout:
        fout.writelines(lines)


def _load(path, f=None):
    with open(path, 'r') as fin:
        return map(f, imap(str.rstrip, fin))


def _load_edges(path):
    wrap = F(flip(str.split), '\t') >> (lambda xs: cn.wrap_edge(*xs))
    return _load(path, wrap)


def handle_split(graph_paths, nodes_path=None, edges_path=None, rels_path=None):
    get_edges = F(cn.iter_edges,
                  normalize=filters.normalize_assertion,
                  prefilter=filters.prefilter_assertion,
                  postfilter=filters.postfilter_assertion) >> tuple
    get_nodes = F(cn.iter_nodes) \
        >> F(cn.iter_filter_with_count, filters.postfilter_concept) \
        >> sorted
    get_rels = F(cn.iter_rels) \
        >> F(cn.iter_filter_with_count, None) \
        >> sorted

    edges = get_edges(graph_paths)
    nodes = get_nodes(edges)
    rels = get_rels(edges)

    if nodes_path is not None:
        _save(nodes_path, nodes)

    if rels_path is not None:
        _save(rels_path, rels)

    edges = sorted(cn.simplify_edges(edges, nodes, rels))
    if edges_path is not None:
        lines = imap('\t'.join, (imap(str, edge) for edge in edges))
        _save(edges_path, lines)


def handle_seed(seed_type, raw_path, seed_path, nodes_path):
    load = {
        'anew': anew.load,
        'sn': sn.load
    }[seed_type]

    nodes = _load(nodes_path)
    seeds = imap(load(raw_path).get, nodes)
    _save(seed_path, seeds)


def handle_iterreg(anew_path, sn_path, edges_path, pred_path, pis_path=None, param=None):
    anew = _load(anew_path, atof)
    sn = _load(sn_path, atof)
    edges = _load_edges(edges_path)

    pis = None
    if pis_path is not None:
        pis = _load(pis_path, atof)

    pred = iterreg(anew, sn, edges, pis, param=param)
    _save(pred_path, pred)


def handle_eval(metric, pred_path, truth_path):
    preds = [p if p is not None else 0.0 for p in _load(pred_path, atof)]
    split = F(flip(str.split), '\t')
    with open(truth_path, 'r') as fin:
        truths = tuple((int(i), int(j)) for i, j in imap(split, fin))

    result = {
        'polarity': polarity_accuracy,
        'kendall': kendall_tau
    }[metric](preds, truths)
    print result
