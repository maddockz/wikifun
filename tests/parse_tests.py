#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'maddockz'

import os.path
from bz2 import BZ2File
import re

import pkg_resources
import subprocess
from nose.tools import *

from wikifun.etl import parse
import wikifun.etl.data_models as dm


def test_extract_text():
    assert True


def test_title_from_text():
    title = parse.title_from_text("heroes are found ' in ' the '''Call of Duty''' ")
    assert title == 'Call of Duty'


def test_categories_from_text():
    text = "blah blah [[Boring]], [[Category: Talk]] grapefruit [[Category: Fruit| ]]"
    categories = parse.categories_from_text(text)
    assert categories[0] == "Talk", "Failure: Category = {0}".format(categories[0])
    assert categories[1] == "Fruit", "Failure: Cateogry = {0}".format(categories[1])


class TestBz2:
    test_file = pkg_resources.resource_filename('wikifun', '../data/sandbox/test.bz2')

    def setUp(self):
        example = ["blah blah blah\n",
                   '<page> \n',
                   "The title of the article is '''TITLE''', yes indeed!\n",
                   "Hamsters can fly.\n",
                   "They really can't.\n",
                   "[[Category:Lies]]\n",
                   "[[Category:Hamsters| ]]\n",
                   "</page>\n",
                   "xxxx<page>\n Page 2 without a title \n </page>"]
        if os.path.isfile(TestBz2.test_file):
            subprocess.call(["rm", TestBz2.test_file])
        with BZ2File(TestBz2.test_file, 'w') as f:
            f.writelines(example)

    def test_title(self):
        with BZ2File(TestBz2.test_file, 'r') as f:
            page = parse.read_page(f)
            title = parse.title_from_text(page)
            assert title == "TITLE", "Page 1 title: {0}".format(title)

            page2 = parse.read_page(f)
            title2 = parse.title_from_text(page2)
            assert len(title2) == 0, "Title not empty, Title: {0}".format(title2)


class TestWikiDumpParsing:
    def setUp(self):
        self.f = BZ2File(parse._wiki_dump_abspath)

    def teardown(self):
        self.f.close()

    def test_first_title(self):
        first_page = parse.read_page(self.f)
        title = parse.extract_title(first_page)
        assertion = (title == "AccessibleComputing")
        assert assertion, 'First title:{0} is not AccessibleComputing'.format(title)

    def test_first_nonempty_article(self):
        text = ''
        title = ''
        while not text:
            page = parse.read_page(self.f)
            title = parse.extract_title(page)
            text = parse.extract_text(page)
        assert title == "Anarchism", "Title is: {0}".format(title)

    def test_unicode_text(self):
        for i in range(50):
            page = parse.read_page(self.f)
            text = parse.extract_text(page)
            assert type(text) == unicode, "Text of type: {0}".format(type(text))

    def test_char_byte_length(self):
        for i in range(50):
            page = parse.read_page(self.f)
            text = parse.extract_text(page)
            title = parse.extract_title(page)
            for char in text:
                msg = u'4 Bytes required: Article {0} contains {1}'.format(title,
                                                                          char)
                assert ord(char) < 256**3, msg


class TestCleaningAndFiltering:
    def setUp(self):
        self.record = {}
        self.record['title'] = 'Title'
        text = 'Here is text.{{cite book}}[[Category:A]] XXX'
        self.record['text'] = text

    def test_clean_text(self):
        record = parse.clean_record(self.record)
        assert record['text'] == 'Here is text.', record['text']