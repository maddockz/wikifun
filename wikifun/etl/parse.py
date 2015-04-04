"""
Created on Mar 28, 2015
Parses XML file, extracting article text and wikipedia categories
@author: maddockz

This module parses a compressed wikipedia dump of format .xml.bz2,
cleans the text (e.g. by removing wikipedia links and external references),
and extracts the categories the article belongs to.  These are then
uploaded into the MySQL database (cf. config.py)

E.g. To parse the first N articles, use the function:
                bz2_to_mysql(limit=N)
Passing no argument parses all articles, and may take a day or two.

This function is called when running module from the command line:
python ./wikifun/etl/parse_xml.py [N]
"""

import re
import sys
from bz2 import BZ2File
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import pkg_resources
import peewee as pw

import wikifun.etl.data_models as dm
import config

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
    :return: dict or None # dict is only returned if error with INSERT article
    """
    dm.db.connect()
    bad_record = False
    try:
        article = dm.Article(title=record['title'], text=record['text'])
        article.save()
    except pw.IntegrityError, e:
        print e
    except pw.OperationalError, e:
        print u'Error with article {0}'.format(record['title'])
        bad_record = True
    else:
        for cat_value in record['cats']:
            try:
                category = dm.Category(value=cat_value)
                category.save()
            except pw.IntegrityError, e:  # If duplicate category
                # Select the category entry already in the table
                category = dm.Category.get(dm.Category.value == cat_value)
            try:
                mapping_table = dm.MappingTable(article=article,category=category)
                mapping_table.save()
            except pw.IntegrityError, e:
                print e
    finally:
        dm.db.close()
    if bad_record:
        return record

def filter_record(record):
    """
    Returns true if the record is dict containing valid
    (non-disambiguation, non-redirect) wikipedia page.
    :param record: dict
    :key title: unicode
    :key text: unicode
    :key cats: list[unicode]
    :return: True
    """
    if re.findall(r'\(disambiguation\)', record['title']):
        return False
    if not record['text']:
        return False
    if not record['title']:
        return False
    return True

def clean_record(record):
    """
    Cleans the wikipedia page text found in record['text'] of formatting
    characters, references, etc.  Side-effect: modifies record.
    :param record: dict
    :key text: unicode
    :return: dict :key text: unicode
    """
    text = record['text']
    # Replace [[<link>|<text>]] with <text>
    text = re.sub(r'\[\[([^\]]{0,255})\|([^\]]{0,255})\]\]',
                  lambda x: x.group(2),
                  text)
    # Remove {{cite| ... }} and {{IPA...}}
    removal_regexp = r'{{[Cc](ite|itation) [^}]+}}'
    removal_regexp += r'|{{IPA[^}{]{0,255}}}'
    text = re.sub(removal_regexp, '', text, flags=re.DOTALL)
    # Removes <ref ...> ... </ref>
    text = re.sub(r'<ref[^>]*(/>|>[^<]*</ref>)',
                  '',
                  text,
                  flags=re.DOTALL)
    # Replace [[<link name>]] with <link name>
    text = re.sub(r'\[\[([^\]]{0,255})\]\]',
                  lambda x: x.group(1),
                  text,
                  flags=re.DOTALL)
    # Replace &nbsp; with ' '
    text = re.sub(r'&nbsp;', ' ', text)
    # Replace &ndash; with ' - '
    text = re.sub(r'&ndash;', ' - ', text)
    # Replace {{lang.##|<text>}} with <text>
    text = re.sub(r'{{lang.{3}\|([^}\|]{0,255})}}',
                  lambda x: x.group(1), text )
    # Remove comments <!--- --->
    text = re.sub(r'<![^>]+>', '', text)
    # Remove formatting strings: style="...", class="..."
    text = re.sub(r'(style|class)\s?="[^"]{0,50}"', '', text)
    # Remove small tags <...>
    text = re.sub(r'<.{0,30}>','', text)

    record['text'] = text
    return record


def bz2_parse(filename=_wiki_dump_abspath, insert_fun=insert_record, limit=1e12):
    """
    Parses a .xml.bz2 file containing wikipedia articles and stores in MySQL
    :param filename: str  # path to .xml.bz2 file
    :param insert_fun: function( list[unicode] )  # to record the articles
    :param limit: int  # Maximum number of articles to output
    :return: list[dict]  # Returns articles not able to be added to MySQL
                           (due to unicode error)
    """
    bad_records = []
    with BZ2File(filename) as f:
        # Read in first page
        page = read_page(f)
        # Create tables if do not exist
        dm.create_tables()

        n = 0
        while page and n < limit:
            record = {'text': extract_text(page), 'title': extract_title(page)}
            record['cats'] = categories_from_text(record['text'])
            # Only pass cleaned records passing filter criteria to insert_fun
            if filter_record(record):
                bad_record = insert_fun(clean_record(record))
                if bad_record:
                    bad_records.append(bad_record)
            page = read_page(f)
            n += 1
    return bad_records

def bz2_to_mysql(filename = _wiki_dump_abspath, limit=1e12):
    """
    Parses a .xml.bz2 file containing wikipedia articles and stores in MySQL
    :param filename: str  # path to .xml.bz2 file
    :param limit: int  # Max number of articles to record
    :return: list[dict]  # list of bad records
    """
    return bz2_parse(filename, insert_record, limit)


def read_page(f):
    """
    Reads next Wikipedia page from BZ2File stream
    :param f: BZ2File
    :return: str  # xml string bounded by <page> tags
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
    try:
        match = re.search(r"^[^{}\|\n].{0,50}'''", raw_text, flags=re.MULTILINE)
    except TypeError, e:
        print "Text is empty."
        match = None
    if match:
        clean_text = raw_text[match.start():].strip()
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
    return re.findall(r'\[\[[Cc]ategory:\s*([^\]\|]*)\s*\|?\s*\]\]', text)


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


if __name__ == '__main__':
    n = 1e12
    if len(sys.argv) > 1:
        n = sys.argv[1]
    bz2_to_mysql(limit=n)
