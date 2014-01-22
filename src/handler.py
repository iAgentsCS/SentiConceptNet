# -*- coding: utf-8 -*-

from itertools import imap
from random import uniform

from fn import F
from fn.op import flip

from numpy import var

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
    'handle_seeds',
    'handle_iterreg',
    'handle_ircert',
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


def handle_split(graph_paths, nodes_path, edges_path, rels_path):
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

    _save(nodes_path, nodes)
    _save(rels_path, rels)

    edges = sorted(cn.simplify_edges(edges, nodes, rels))
    lines = imap('\t'.join, (imap(str, edge) for edge in edges))
    _save(edges_path, lines)


def handle_seeds(source, raw_path, seed_path, nodes_path):
    load = {
        'anew': anew.load,
        'sn': sn.load
    }[source]

    nodes = _load(nodes_path)
    seeds = imap(load(raw_path).get, nodes)
    _save(seed_path, seeds)


def handle_iterreg(anew_path, sn_path, edges_path, pred_path, pis_path=None,
                   param=None):
    anew = _load(anew_path, atof)
    sn = _load(sn_path, atof)
    edges = _load_edges(edges_path)

    pis = None
    if pis_path is not None:
        pis = _load(pis_path, atof)

    pred = iterreg(anew, sn, edges, pis, param)
    _save(pred_path, pred)


def handle_ircert(pred_paths, cert_path):
    val_list = []
    for path in pred_paths:
        preds = _load(path, atof)
        preds = [v if v is not None else uniform(-1, 1) for v in preds]
        val_list.append(preds)

    preds = _load(pred_paths[-1], atof)
    var_list = var(val_list, 0)

    certs = [1 / v if preds[i] is not None else 0.0
             for i, v in enumerate(var_list)]

    _save(cert_path, certs)


def handle_randwalk(edges_path, seed_path, pred_path, alpha, axis,
                    cert_in_path, cert_out_path):
    values = _load(seed_path, atof)
    seeds = [p if p is not None else 0.0 for p in values]
    certs = _load(cert_in_path, float)

    graph = load_graph(edges_path, axis)
    pred, certs = random_walk(graph, seeds, certs, alpha)
    _save(pred_path, pred)
    _save(cert_out_path, certs)


def handle_shift(strategy, seed_path, pred_in_path, pred_out_path):
    pred_in = _load(pred_in_path, atof)
    seeds = _load(seed_path, atof)
    shift = {
        'za': align_zero,
        'mva': align_mean_var
    }[strategy]

    pred_in = [v if v != 0.0 else None for v in pred_in]
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


def handle_lookup(nodes_path, anew_path, sn_path, pred_path,
                  rels_path, edges_path):
    nodes = _load(nodes_path)
    anew = _load(anew_path, atof)
    sn = _load(sn_path, atof)
    pred = _load(pred_path, atof)
    rels = _load(rels_path)
    edges = _load_edges(edges_path)
    lookup(nodes, anew, sn, pred, rels, edges)
