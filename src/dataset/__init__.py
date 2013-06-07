#!/usr/bin/env python
# -*- coding: utf-8 -*-


def atof(text):
    return float(text) if text != 'None' else None


def load(path, parser, key, value):
    return dict((key(instance), value(instance)) for instance in parser(path))
