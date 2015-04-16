#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Running etl module from command-line will create database using information
from config.py and begin uploading articles.  This module takes one
command-line argument, which provides a bound on the number of articles to
import.
"""
__author__ = 'maddockz'

import sys

import data_models as dm
import parse
import label
import word_count as wc

if __name__=='__main__':
    if len(sys.argv) == 1:
        limit = 1e9
        print "No Limit"
    else:
        limit = int(sys.argv[1])
        print "Limit = {0}".format(limit)

    dm.create_database()
    dm.create_tables()
    parse.bz2_to_mysql(limit=limit)
    wc.tabulate_articles(start=0, stop=limit)
    label.label_history()


