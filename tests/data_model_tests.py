"""
Tests for integrity of data models.
"""
__author__ = 'maddockz'

import re

import peewee as pw

import wikifun.etl.data_models as dm

class TestDatabaseConnection:
    def setUp(self):
        dm.db.connect()

    def teardown(self):
        dm.db.close()

    def test_create_table(self):
        dm.create_tables()
        tables = dm.db.get_tables()
        for table in [u'article', u'category', u'mappingtable']:
            assert table in tables, "missing TABLE {0}".format(table)

    def test_for_Apollo_article(self):
        try:
            dm.Article.get(dm.Article.title==u'Apollo')
        except dm.Article.DoesNotExist, e:
            assert False, e
        else:
            assert True

    def test_disambiguation_category_removal(self):
        # Tests if any articles are disambiguations
        try:
            a = dm.Article.get(dm.Article.title % '%disambiguation%')
        except pw.DoesNotExist:
            assert True
        else:
            assert False, "Disambiguation exists: {0}".format(a.title)

    def test_administrative_article_removal(selfs):
        # Tests if any articles are of form 'Wikipedia:...'
        try:
            a = dm.Article.get(dm.Article.title % 'Wikipedia:%')
        except pw.DoesNotExist:
            assert True
        else
            assert False, "Admin article: {0}".format(a.title)
