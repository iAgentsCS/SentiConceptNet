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
    parser_sd.add_argument('--type', dest='seed_type', choices=('anew', 'sn'), required=True)
    parser_sd.add_argument('--raw', dest='raw_path', required=True)
    parser_sd.add_argument('--seed', dest='seed_path', required=True)
    parser_sd.add_argument('--nodes', dest='nodes_path', required=True)

    args = vars(parser.parse_args())
    handler = args.pop('handler')
    handler(**args)


if __name__ == '__main__':
    main()
