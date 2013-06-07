#!/usr/bin/env python
# -*- coding: utf-8 -*-


def polarity_accuracy(preds, truths):
    n = len(truths)
    t = sum(preds[i] * p > 0 for i, p in truths)
    return float(t) / n


def kendall_tau(preds, truths):
    n = len(truths)
    t = sum(preds[i] <= preds[j] for i, j in truths)
    return float(t) / n
