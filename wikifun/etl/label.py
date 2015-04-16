#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Labels the articles in the database that have the keyword 'history' in one
of their categories"""
__author__ = 'maddockz'

import MySQLdb as msdb

import config

def label_history():
    """
    Sets the is_history label to True where category LIKE '%history%'.
    :return: None
    """
    db = msdb.connect(**config.database)
    c = db.cursor()
    c.execute("""UPDATE article
              SET is_history = TRUE
              WHERE id IN (
              SELECT article_id FROM mappingtable
              INNER JOIN category ON category_id = category.id
              WHERE value LIKE '%history%')""")
    db.commit()
    db.close()

