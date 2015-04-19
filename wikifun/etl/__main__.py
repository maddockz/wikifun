#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Warning: Running this module from command line will first drop all tables in
database.

Then will create database using information from config.py and begin
uploading articles.  Will also generate simple random train and test samples,
computing word frequencies for all articles in samples, before caching
the results.

This module takes one command-line argument, which provides a bound on the
number of articles to import.
"""
__author__ = 'maddockz'

import sys

import data_models as dm
import parse
import label
import sample

if __name__=='__main__':
    if len(sys.argv) == 1:
        limit = 1e9
        print "No Limit"
    else:
        limit = int(sys.argv[1])
        print "Limit = {0}".format(limit)

    dm.create_database()
    dm.drop_tables()
    dm.create_tables()
    parse.bz2_to_mysql(limit=limit)
    sample.main()
    label.label_history()


