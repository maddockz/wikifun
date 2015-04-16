#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module for computing word frequencies in Wikipedia articles in MySQL database.
"""

import re
from collections import defaultdict

import numpy as np
import peewee as pw

import wikifun.etl.data_models as dm

__author__ = 'maddockz'

def count(text):
    """
    Tabulates a count of the words in text, separated by punctuation.
    :param text: unicode
    :return: dict of [unicode, int]
    """
    word_list = re.split('\W+', text)
    d = defaultdict(int)
    for word in word_list:
        d[word.lower()] += 1
    return d

def record(article, word, freq):
    """
    Stores word and frequency in database, linking to article.
    Only creates new entry for word if it does not previously appear.
    (Warning: MySQL's unicode difficulties creates Python overhead)
    :param article: dm.Article
    :param word: unicode
    :param freq: int
    :return: None
    """
    try:
        dm.db.connect()
        if not word:
            raise TypeError, "word string is empty or None"
        w = None
        for this_word in dm.Word.select().where(dm.Word.value==word).iterator():
            if this_word.value == word:  #Needed b/c MySQL thinks 'e' = 'é'
                w = this_word
        if not w:
            w = dm.Word(value=word)
            w.save()

        word_freq = dm.WordFreq(word=w, article=article,freq=freq)
        word_freq.save()
    except TypeError:
        return
    finally:
        dm.db.close()

def tabulate_articles(start=0, stop=10):
    """
    Iterates over all articles between start and stop in database, tabulates
    word frequencies, and stores the counts.
    Side-effects: prints iteration indices to stdout
    :param start: int
    :param stop: int
    :return: None
    """
    i = -1
    for article in dm.Article.select().limit(stop):
        i += 1
        if i < start:
            continue
        word_freqs = count(article.text)
        article.length = len(word_freqs)
        article.update()
        for word, freq in word_freqs.iteritems():
            record(article, word, freq)
        print i,
        if i % 20 == 0:
            print '\n',

def compute_idf():
    """
    Returns the (log) inverse document frequency for each word
    :return: dict of [dm.Word, float]
    """
    count_query = pw.fn.Count(fn.Distinct(dm.WordFreq.article))
    tot_articles = dm.WordFreq.select(count_query).scalar()
    idf_dict = {}
    for word in dm.Word.select().iterator():
        condition = (dm.WordFreq.word == word)
        n_docs = dm.WordFreq.select().count().where(condition).scalar()
        try:
            idf = np.log(1.0 * tot_articles/n_docs)
        except ZeroDivisionError:
            idf = 0
        idf_dict[word] = idf
    return idf_dict


def compute_max_freq(article):
    """
    Returns the frequency of the most common word in the article.
    :param article: dm.Article
    :return: int
    """
    pass
