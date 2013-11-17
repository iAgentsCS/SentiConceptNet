# -*- coding: utf-8 -*-

from collections import namedtuple, defaultdict
from math import copysign

__all__ = (
    'generate_features',
    'encode_features'
)

_SelfFeatures = namedtuple('SelfFeatures', ('sentiment', 'polarity'))
_NeighborFeatures = namedtuple(
    'NeighborFeatures',
    ('direction', 'relation', 'weight', 'anew', 'sn', 'pis')
)


def _none2f(value):
    return value if value is not None else 0.0


def _sign(value):
    return 0 if (value is None) else int(copysign(1.0, value))


def _interval(value):
    if value is None:
        #itv = 11
        itv = None
    else:
        itv = max(0, min(10, int(value * 5.0) + 5))

    return itv


def _get_neighbor_tuple(neighbor, seed):
    seed_id = {
        'anew': 0,
        'sn': 1,
        'pis': 2
    }[seed]
    return (seed_id, neighbor.direction, neighbor.relation, neighbor[3 + seed_id])


def generate_features(anew, sn, edges, pis=None):
    if pis is None:
        pis = (None,) * len(anew)

    features = [{
        'self': _SelfFeatures(_none2f(sentiment), _sign(sentiment)),
        'neighbor': [],
        'weight_sum': {'anew': 0.0, 'sn': 0.0, 'pis': 0.0}
    } for sentiment in sn]

    for edge in edges:
        rel, start, end, _ = edge
        weight = 1.0

        features[start]['neighbor'].append(
            _NeighborFeatures(
                0, rel, weight,
                _interval(anew[end]),
                _interval(sn[end]),
                _interval(pis[end])
            )
        )
        features[end]['neighbor'].append(
            _NeighborFeatures(
                1, rel, weight,
                _interval(anew[start]),
                _interval(sn[start]),
                _interval(pis[start])
            )
        )

        if anew[start] is not None:
            features[end]['weight_sum']['anew'] += weight
        if sn[start] is not None:
            features[end]['weight_sum']['sn'] += weight
        if pis[start] is not None:
            features[end]['weight_sum']['pis'] += weight

        if anew[end] is not None:
            features[start]['weight_sum']['anew'] += weight
        if sn[end] is not None:
            features[start]['weight_sum']['sn'] += weight
        if pis[end] is not None:
            features[start]['weight_sum']['pis'] += weight

    return features


def _polarity(itv):
    if itv == 5:
        return 0
    if itv > 5:
        return 1
    if itv < 5:
        return 2


def encode_features(features):
    # [TODO] avoid magic numbers
    neighbor_type_number = 3 * 2 * 12 * 33

    for feature in features:
        encoded_feature = defaultdict(float)

        neighbor_features = feature['neighbor']
        weight_sum = feature['weight_sum']
        for neighbor in neighbor_features:
            weight = neighbor.weight

            if neighbor.anew is not None:
                index = 0 * 2 * 12 * 33 + neighbor.direction * 12 * 33 + neighbor.relation * 12 + neighbor.anew
                encoded_feature[index] += weight / weight_sum['anew']
            if neighbor.sn is not None:
                index = 1 * 2 * 12 * 33 + neighbor.direction * 12 * 33 + neighbor.relation * 12 + neighbor.sn
                encoded_feature[index] += weight / weight_sum['sn']
            if neighbor.pis is not None:
                index = 2 * 2 * 12 * 33 + neighbor.direction * 12 * 33 + neighbor.relation * 12 + neighbor.pis
                encoded_feature[index] += weight / weight_sum['pis']

        self_features = feature['self']
        if self_features.polarity != 0:
            encoded_feature[neighbor_type_number + 0] = self_features.sentiment
            encoded_feature[neighbor_type_number + 1] = self_features.polarity

        yield encoded_feature
