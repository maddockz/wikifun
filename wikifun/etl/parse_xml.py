"""
Created on Mar 28, 2015
Parses XML file, extracting article text and wikipedia categories
@author: maddockz
"""

import re
from bz2 import BZ2File
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import pkg_resources
import peewee as pw

import config
import wikifun.etl.data_models as dm

_wiki_dump = config.WIKI_DUMP_FILENAME
_wiki_dump_abspath = pkg_resources.resource_filename('wikifun',
                                                     "../data/" + _wiki_dump)

def insert_record(record):
    """
    INSERT record into MySQL database
    :param record: dict
    :key title: unicode
    :key text: unicode
    :key cats: list[unicode]
    :return: None
    """
    dm.db.connect()
    try:
        print record['title'], record['cats']  # For TESTING
        article = dm.Article(title=record['title'], text=record['text'])
        article.save()
        for cat_value in record['cats']:
            category = dm.Category(value=cat_value)
            category.save()
            mapping_table = dm.MappingTable(article=article,
                                            category=category)
            mapping_table.save()
    except pw.IntegrityError, e:
        print e
    except pw.OperationalError, e:
        print u'Error with article {0}'.format(record['title'])
        # raise e
    finally:
        dm.db.close()

def bz2_parse(filename=_wiki_dump_abspath, insert_fun=insert_record, limit=1e30):
    """
    Parses a .xml.bz2 file containing wikipedia articles and stores in MySQL
    :param filename: str # path to .xml.bz2 file
    :param insert_fun: function( list[unicode] ) # to record the articles
    :param limit: int # Maximum number of articles to output
    :return: None
    """
    with BZ2File(filename) as f:
        # Read in first page
        page = read_page(f)
        # Create tables if do not exist
        dm.create_tables()

        n = 0
        while page and n < limit:
            record = {'text': extract_text(page), 'title': extract_title(page)}
            record['cats'] = categories_from_text(record['text'])
            # INSERT only if article text is not empty
            if record['text']:
                insert_fun(record)
            page = read_page(f)
            n += 1


def bz2_to_mysql(filename = _wiki_dump_abspath, limit=1e30):
    """
    Parses a .xml.bz2 file containing wikipedia articles and stores in MySQL
    :param filename: str # path to .xml.bz2 file
    :param limit: int # Max number of articles to record
    :return: None
    """
    bz2_parse(filename, insert_record, limit)


def read_page(f):
    """
    Reads next Wikipedia page from BZ2File stream
    :param f: BZ2File
    :return: str # xml string bounded by <page> tags
    Caveat: Returns '' if no pages found
    """
    lines = []
    page_open = False
    # Discard lines until <page> or EOF is encountered
    while not page_open:
        line = f.readline()
        if re.findall('<page>', line):
            page_open = True
            lines.append('<page>')
        if not line:
            break  # EOF reached
    # Store lines until after </page> encountered
    while page_open:
        line = f.readline()
        if re.findall('</page>', line):
            page_open = False
        if not line:
            print "Warning: EOF reached within <page> environment"
            break
        lines.append(line)
    return '\n'.join(lines)


def extract_text(xml_string):
    """
    Extracts the text from XML page string
    :type xml_string: str # a single wikipedia XML page
    :return: unicode # the raw text of the wikipedia article
    """
    root = et.fromstring(xml_string)
    raw_text = root.find('./revision/text').text
    # Remove meta data before article text
    match = re.search("\'\'\'", raw_text)
    if match:
        clean_text = raw_text[match.start():]
        if type(clean_text) is not unicode:
            clean_text = unicode(clean_text, 'utf-8')
    else:
        clean_text = u''
    return clean_text


def categories_from_text(text):
    """
    Extracts a list of categories from the text of a Wikipedia article
    :param text: str # Wikipedia article raw text
    :return: list[str] # Categories
    """
    # Categories appear at end of text in formats:
    # [[Category:<name>]]
    # [[Category:<name>| ]] (in case <name> is article title)
    return re.findall('\[\[[Cc]ategory:\s*([^\]\|]*)\s*\|?\s*\]\]', text)


def extract_title(xml_string):
    """
    Extracts the title from XML Wikipedia page string
    :param xml_string: unicode
    :return: unicode
    """
    root = et.fromstring(xml_string)
    title = root.find('./title').text
    if type(title) is not unicode:
        title = unicode(title, 'utf-8')
    return title


def title_from_text(text):
    """
    Deprecated: Instead use extract_title.
    Extracts the title of a Wikipedia article from its raw text
    :param text: str # Wikipedia article raw text
    :return: str # title of article
    """
    # Title of article is given in first line of text in triple single-quotes
    match_list = re.findall("'''(.*)'''", text)
    try:
        return match_list[0]
    except IndexError:
        return ''


