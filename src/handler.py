# -*- coding: utf-8 -*-

from itertools import imap
from random import uniform

from fn import F
from fn.op import flip

import dataset.anew as anew
import dataset.senticnet as sn
import dataset.conceptnet as cn
import dataset.filters as filters

from dataset import atof
from iterreg import iterreg
from randwalk import load_graph, random_walk
from shift import align_zero, align_mean_var
from eval import polarity_accuracy, kendall_tau
from lookup import lookup

__all__ = (
    'handle_split',
    'handle_seed',
    'handle_iterreg',
    'handle_randwalk',
    'handle_shift',
    'handle_eval',
    'handle_lookup'
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


def handle_seed(type, raw_path, seed_path, nodes_path):
    load = {
        'anew': anew.load,
        'sn': sn.load
    }[type]

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


def handle_randwalk(edges_path, seed_path, certainty_in_path,
                    pred_path, certainty_out_path, alpha, axis):
    values = _load(seed_path, atof)
    seeds = [p if p is not None else 0.0 for p in values]
    confidences = _load(certainty_in_path, float)

    graph = load_graph(edges_path)
    pred, confidences = random_walk(graph, seeds, confidences, alpha, axis)
    _save(pred_path, pred)
    _save(certainty_out_path, confidences)


def handle_shift(strategy, seed_path, pred_in_path, pred_out_path):
    pred_in = _load(pred_in_path, atof)
    seeds = _load(seed_path, atof)
    shift = {
        'za': align_zero,
        'mva': align_mean_var
    }[strategy]

    pred_out = shift(pred_in, seeds)
    _save(pred_out_path, pred_out)


def handle_eval(metric, pred_path, truth_path):
    preds = _load(pred_path, atof)
    split = F(flip(str.split), '\t')
    with open(truth_path, 'r') as fin:
        truths = tuple((int(i), int(j)) for i, j in imap(split, fin))

    result = {
        'polarity': polarity_accuracy,
        'kendall': kendall_tau
    }[metric](preds, truths)
    print result


def handle_lookup(nodes_path, anew_path, sn_path, pred_path, rels_path, edges_path):
    nodes = _load(nodes_path)
    anew = _load(anew_path, atof)
    sn = _load(sn_path, atof)
    pred = _load(pred_path, atof)
    rels = _load(rels_path)
    edges = _load_edges(edges_path)
    lookup(nodes, anew, sn, pred, rels, edges)
