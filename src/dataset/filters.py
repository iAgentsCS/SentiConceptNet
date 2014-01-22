# -*- coding: utf-8 -*-


def prefilter_concept(concept):
    return concept.startswith('/c/en/')


def prefilter_assertion(assertion):
    rel = assertion['rel']
    start = assertion['start']
    end = assertion['end']
    return prefilter_concept(start) and prefilter_concept(end) \
        and rel.startswith('/r/') and start != end


def postfilter_concept(concept):
    #return concept.count > 1 and concept.text
    return concept.text


def postfilter_assertion(assertion):
    #return assertion['count'] > 1 and assertion['weight'] > 0.0
    return assertion['weight'] > 0.0


def normalize_concept(concept):
    return concept.split('/')[3]


def normalize_assertion(assertion):
    assertion['rel'] = assertion['rel'].split('/')[2]
    assertion['start'] = normalize_concept(assertion['start'])
    assertion['end'] = normalize_concept(assertion['end'])
    #assertion['weight'] /= assertion['count']
    return assertion
