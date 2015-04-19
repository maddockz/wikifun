#!/usr/bin/env python
# -*- coding:utf-8 -*_
"""
Generate plots for validating the naive bayes model in idiots_bayes.py.
Requires previously cached indices for training and test data
"""
__author__ = 'maddockz'

import roc
import wikifun.model.idiots_bayes as ib
import wikifun.etl.sample as sample


def roc_curve(limit = int(1e9)):
    nb_fit = ib.main(limit)
    train_ids, test_ids = sample.get_cached_ids()
    test = sample.get_articles(test_ids[:limit])
    X = ib.make_X(test)
    y = ib.make_y(test)
    log_probas = nb_fit.predict_log_proba(X)[:,1]
    roc.plot_all([("Naive Bayes", y, log_probas)])


if __name__ == '__main__':
    roc_curve()