__author__ = 'maddockz'

from nose.tools import *
from wikifun.etl import parse_xml
from bz2 import BZ2File
import pkg_resources
import subprocess
import os.path

def test_extract_text():
    # Assert that 83 articles are extracted from our sandbox data set
    assert True

def test_title_from_text():
    title = parse_xml.title_from_text("heroes are found ' in ' the '''Call of Duty''' ")
    assert title == 'Call of Duty'

def test_categories_from_text():
    text = "blah blah [[Boring]], [[Category: Talk]] grapefruit [[Category: Fruit| ]]"
    categories = parse_xml.categories_from_text(text)
    assert categories[0] == "Talk", "Failure: Category = {0}".format(categories[0])
    assert categories[1] == "Fruit", "Failure: Cateogry = {0}".format(categories[1])

class TestBz2:
    test_file = pkg_resources.resource_filename('wikifun', '../data/sandbox/test.bz2')
    def setUp(self):
        example = ["blah blah blah\n",
                   '<page> \n',
                   "The title of the article is '''TITLE''', yes?\n",
                   "hamsters can fly.\n",
                   "they really can't.\n",
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
            page = parse_xml.extract_page(f)
            title = parse_xml.title_from_text(page)
            assert title == "TITLE", "Page 1 title: {0}".format(title)

            page2 = parse_xml.extract_page(f)
            title2 = parse_xml.title_from_text(page2)
            assert len(title2) == 0, "Title not empty, Title: {0}".format(title2)
