#!/usr/bin/env python
# -*- coding:utf-8 -*_
"""
Generate plots for validating naive bayes model in idiots_bayes.py
"""
__author__ = 'maddockz'

import roc
import wikifun.model.idiots_bayes as ib
import wikifun.etl.sample as sample


def roc_curve():
    nb_fit = ib.main()
    train_ids, test_ids = sample.get_cached_ids()
    test = sample.get_articles(test_ids)
    X = ib.make_X(test)
    y = ib.make_y(test)
    roc.plot_all([("train", y, nb_fit.predict_log_proba(X) )])


if __name__ == '__main__':
    roc_curve()