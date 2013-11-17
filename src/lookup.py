# -*- coding: utf-8 -*-

from sys import stderr

__all__ = ('lookup',)


def lookup(nodes, anew, sn, pred, rels, edges):
    idx_map = dict((c, i) for i, c in enumerate(nodes))
    while True:
        target = raw_input('>>> ').strip().replace(' ', '_')
        if not target:
            continue

        try:
            idx = idx_map[target]
        except KeyError:
            stderr.write('[ERROR] concept "{0}" doesn\'t exist.\n'.format(target))
            continue

        self_loops = []
        start_assertions = []
        end_assertions = []
        for assertion in edges:
            if assertion.start == idx and assertion.end == idx:
                self_loops.append(assertion)
            elif assertion.start == idx:
                start_assertions.append(assertion)
            elif assertion.end == idx:
                end_assertions.append(assertion)

        print 'Informations:'
        print '\tSentiment (ANEW): {0}'.format(anew[idx])
        print '\tSentiment (SN)  : {0}'.format(sn[idx])
        print '\tSentiment (PRED): {0}'.format(pred[idx])

        print 'Self Loops ({0}):'.format(len(self_loops))
        for self_loop in self_loops:
            print '\t({0}, {1})'.format(rels[self_loop.rel], self_loop.weight)

        print 'Start Assertions ({0}):'.format(len(start_assertions))
        for start_assertion in start_assertions:
            rel = start_assertion.rel
            end = start_assertion.end
            weight = start_assertion.weight
            print '\t({0} {1}, {2}) - ({3}, {4}, {5})' \
                .format(rels[rel], nodes[end], weight, anew[end], sn[end], pred[end])

        print 'End Assertions ({0}):'.format(len(end_assertions))
        for end_assertion in end_assertions:
            rel = end_assertion.rel
            start = end_assertion.start
            weight = end_assertion.weight
            print '\t({0} {1}, {2}) - ({3}, {4}, {5})' \
                .format(nodes[start], rels[rel], weight, anew[start], sn[start], pred[start])
