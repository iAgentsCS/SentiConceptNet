#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from handler import *


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_sp = subparsers.add_parser('split')
    parser_sp.set_defaults(handler=handle_split)
    parser_sp.add_argument('--graph', dest='graph_paths', nargs='+', required=True)
    parser_sp.add_argument('--nodes', dest='nodes_path')
    parser_sp.add_argument('--edges', dest='edges_path')
    parser_sp.add_argument('--rels', dest='rels_path')

    parser_sd = subparsers.add_parser('seed')
    parser_sd.set_defaults(handler=handle_seed)
    parser_sd.add_argument('type', choices=('anew', 'sn'))
    parser_sd.add_argument('--raw', dest='raw_path', required=True)
    parser_sd.add_argument('--seed', dest='seed_path', required=True)
    parser_sd.add_argument('--nodes', dest='nodes_path', required=True)

    parser_ir = subparsers.add_parser('iterreg')
    parser_ir.set_defaults(handler=handle_iterreg)
    parser_ir.add_argument('--anew', dest='anew_path', required=True)
    parser_ir.add_argument('--sn', dest='sn_path', required=True)
    parser_ir.add_argument('--edges', dest='edges_path', required=True)
    parser_ir.add_argument('--pis', dest='pis_path')
    parser_ir.add_argument('--pred', dest='pred_path', required=True)
    parser_ir.add_argument('--param')

    parser_rw = subparsers.add_parser('randwalk')
    parser_rw.set_defaults(handler=handle_randwalk)
    parser_rw.add_argument('--edges', dest='edges_path', required=True)
    parser_rw.add_argument('--seed', dest='seed_path', required=True)
    parser_rw.add_argument('--pred', dest='pred_path', required=True)
    parser_rw.add_argument('--alpha', default=0.5, type=float)
    parser_rw.add_argument('--axis', default=1, type=int)

    parser_ev = subparsers.add_parser('eval')
    parser_ev.set_defaults(handler=handle_eval)
    parser_ev.add_argument('metric', choices=('polarity', 'kendall'))
    parser_ev.add_argument('--pred', dest='pred_path', required=True)
    parser_ev.add_argument('--truth', dest='truth_path', required=True)

    args = vars(parser.parse_args())
    handler = args.pop('handler')
    handler(**args)


if __name__ == '__main__':
    main()
