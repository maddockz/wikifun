'''
Created on Mar 28, 2015
Parses XML file, extracting article text and wikipedia categories
@author: maddockz
'''

import pkg_resources
import re
from bz2 import BZ2File
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


_wiki_dump = "enwiki-20150304-pages-articles.xml.bz2"
wiki_dump_filename = pkg_resources.resource_filename('wikifun',
                                                     "../data/" + _wiki_dump)

def bz2_to_mysql(filename):
    """
    Parses a .xml.bz2 file containing wikipedia articles and stores in MySQL
    :param filename: str # path to .xml.bz2 file
    :return: None
    """
    with BZ2File(filename) as f:
        page = read_page(f)
        N = 0 ## REMOVE N LATER
        while page and N < 100:
            text = extract_text(page)
            title = extract_title(page)
            cats = categories_from_text(text)
            try:
                # INSERT only if article text is not empty
                if text:
                    print 'TEXT ACCEPTED FROM: {0}'.format(title)
                    print 'TEXT IS TYPE: {0}'.format(type(text))
                    insert_record(title,text,cats)
            except:
                "Error INSERTing article '{0}'".format(title)
            page = read_page(f)
            N += 1

def read_page(f):
    """
    Reads next wikipedia page from BZ2File stream
    :param f: BZ2File
    :return: str # xml string bounded by <page> tags
    Caveat: Returns '' if no pages found
    """
    lines = []
    page_open = False
    # Discard lines until <page> or EOF is encountered
    while not page_open:
        line = f.readline()
        if(re.findall('<page>',line)):
            page_open = True
            lines.append('<page>')
        if not line:
            break # EOF reached
    # Store lines until after </page> encountered
    while page_open:
        line = f.readline()
        if(re.findall('</page>', line)):
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
    root = ET.fromstring(xml_string)
    raw_text = root.find('./revision/text').text
    ## Remove meta data before article text
    match = re.search("\'\'\'", raw_text)
    if match:
        clean_text = unicode(raw_text[match.start():])
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
    root = ET.fromstring(xml_string)
    return unicode(root.find('./title').text)

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

def insert_record(title, text, cats):
    """
    INSERT entry into MySQL database
    :param title: str
    :param text: str
    :param cats: list[str]
    :return: None
    """
    print u"Title:{0}, Cats:{1},\n Text:{2}...".format(title, cats,
                                                      text[:80].replace('\n',''))
    pass

