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


## About 10000 lines of XML from Wikipedia
xml_file = pkg_resources.resource_filename('wikifun', "../data/sandbox/tenk.xml")

def bz2_to_mysql(filename):
    """
    Parses a .xml.bz2 file containing wikipedia articles and stores in MySQL
    :param filename: str # path to .xml.bz2 file
    :return: None
    """
    with BZ2File(filename) as f:
        page = extract_page(f)
        while page:
            text = extract_text(page)
            title = title_from_text(text)
            cats = categories_from_text(text)
            try:
                insert_record(title,text,cats)
            except:
                "Error INSERTing article '{0}'".format(title)
            page = extract_page(f)

def extract_page(f):
    """
    Extracts next wikipedia page from BZ2File stream
    :param f: BZ2File
    :return: str # xml string found between <page> tags
    E.g. <page> [return-me] </page>
    Caveat: Returns None if no pages found
    """
    lines = []
    page_open = False
    # Discard lines until <page> or EOF is encountered
    while not page_open:
        line = f.readline()
        if(re.findall('<page>',line)):
            page_open = True
        if not line:
            break # EOF reached
    # Store lines until </page> or EOF is encountered
    while page_open:
        line = f.readline()
        if(re.findall('</page>', line)):
            page_open = False
        else:
            lines.append(line)
        if not line:
            print "Warning: EOF reached within <page> environment"
            break
    return '\n'.join(lines)


def extract_text(xml_string):
    """
    Extracts the text from XML page string
    :type filename: str # a wikipedia XML page
    :return: str # the raw text of the wikipedia article
    """
    return xml_string

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

def title_from_text(text):
    """
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
    print "Title:{0}, Cats:{1}, Text:{2}...".format(title, cats, text[:15])
    pass
