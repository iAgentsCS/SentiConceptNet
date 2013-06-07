#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load(path, parser, key, value):
    return dict((key(instance), value(instance)) for instance in parser(path))
