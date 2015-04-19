#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Module for generating training and testing samples from article database,
and ensuring that all statistics are computed for these samples.
"""

__author__ = 'maddockz'

import random
import sys
import pickle
import pkg_resources as pkgr

import MySQLdb as msdb

import config
import wikifun.etl.data_models as dm
import wikifun.etl.word_count as wc

default_train = 10000
default_test = 10000

_data_path = pkgr.resource_filename('wikifun','../data/')

def create_train_test_ids(n_train=default_train, n_test=default_test):
    """
    Returns tuple of (non-overlapping) train indices and test indices,
    (simply) randomly sampled from total number of articles
    :param n_train:
    :param n_test:
    :return: tuple of (list, list), where each list of [int]
    """
    random.seed(777)
    db = msdb.connect(**config.database)
    cur = db.cursor()
    cur.execute('SELECT COUNT(*) FROM article')
    n_total = cur.fetchone()[0]
    db.close()

    total_idx = random.sample(xrange(n_total), n_train + n_test)
    train_ids = total_idx[0:n_train]
    test_ids = total_idx[n_train:n_test + n_train]
    return train_ids, test_ids

def get_articles(ids):
    """
    Returns articles with given ids.
    :param idx: list [int]
    :return: list [dm.Article]
    """
    return [dm.Article.get(dm.Article.id == id) for id in ids]

def create_train_test(n_train=default_train, n_test=default_test):
    """
    Returns a tuple consisting of a train and test data set of articles.
    :param n_train: int
    :param n_test: int
    :return: tuple of (list, list), where each list of [dm.Article]
    """
    train_idx, test_idx = create_train_test_ids(n_train, n_test)
    train = get_articles(train_idx)
    test = get_articles(test_idx)
    return train, test

def get_cached_ids():
    """
    Returns tuple consisting of train and test datasets stored in a pickle
    files data/train.p and data/test.p
    :return: tuple (list, list)
    """
    train_ids = pickle.load(open(_data_path + 'train.p', 'r'))
    test_ids = pickle.load(open(_data_path + 'test.p', 'r'))
    return train_ids, test_ids

def compute_features(ids):
    """
    Computes the word frequencies on articles in idx and updates database.
    :param idx: list [int]
    :return: None
    """
    for article in get_articles(ids):
        print article.title
        wc.tabulate(article)

def main():
    """
    Computes the word frequencies (i.e. features) for each of the articles in
    the training and test datasets, and stores the computations in the MySQL
    database.
    :param: Takes either
             - two system int params for size of train/test sets
             - one system parameter '-p' to indicate previously pickled sets
             - no parameters will use default_train and default_test sizes
    :Side-effects: Updates MySQL database
                   Writes to files data/train.p and data/test.p
    :return: None
    """
    # Generate train and test article ids or load pickled version
    if len(sys.argv) > 2:
        n_train = int(sys.argv[1])
        n_test = int(sys.argv[2])
        train_ids, test_ids = create_train_test_ids(n_train, n_test)
    elif len(sys.argv) == 2 and sys.argv[1] == '-p':
        train_ids, test_ids = get_cached_ids()
    else:
        train_ids, test_ids = create_train_test_ids()
        # Store these default lists for later use
        pickle.dump(train_ids, open(_data_path + 'train.p', 'w'))
        pickle.dump(test_ids, open(_data_path + 'test.p', 'w'))

    # Compute the word frequency features for training and test sets
    compute_features(train_ids + test_ids)

if __name__ == '__main__':
    main()
