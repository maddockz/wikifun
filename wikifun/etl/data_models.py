"""
Data models for wikipedia articles
"""
__author__ = 'maddockz'

import peewee as pw
import MySQLdb as msdb
import config

_config = {key: config.database[key] for key in filter(lambda x: x is not 'db',
                                                        config.database.keys())}
try:
    db = pw.MySQLDatabase(config.database['db'], **_config)
except Exception:
    print "{0} cannot connect to {1}".format(config.database['user'],
                                             config.database['host'])
    raise Exception


class BaseModel(pw.Model):
    class Meta:
        database = db


class Article(BaseModel):
    title = pw.CharField(null=False)
    text = pw.TextField()
    length = pw.IntegerField(null=True)
    is_history = pw.BooleanField(null=True)
    is_sports = pw.BooleanField(null=True)


class Category(BaseModel):
    value = pw.CharField(unique=True, null=False)


class MappingTable(BaseModel):
    article = pw.ForeignKeyField(Article)
    category = pw.ForeignKeyField(Category)

class Word(BaseModel):
    value = pw.CharField(unique=True, null=False)
#    idf = pw.FloatField(null=True)


class WordFreq(pw.Model):
    # In peewee 2.5.1, there is a rather obnoxious inconsistency when using
    # CompositeKeys comprising multiple foreign keys:
    #     In particular, it changes the way one references foreign fields.
    #     Reference is now by id and not by object.
    # E.g. type(WordFreq.article) == int and != Article
    article = pw.ForeignKeyField(Article)
    word = pw.ForeignKeyField(Word)
    freq = pw.IntegerField(null=False)
 #   max_freq = pw.IntegerField(null=True)
    class Meta:
        database = db
        primary_key = pw.CompositeKey('article','word')



def create_tables():
    """
    Creates tables if do not exist
    :return: None
    """
    db.connect()
    for model in [Article, Category, MappingTable, Word, WordFreq]:
        try:
            model.create_table()
        except pw.OperationalError, err:
            "Table {0} already exists".format(str(model))
    db.close()

def create_database():
    """
    Creates the MySQL database 'wikifun'.  Throws msdb.ProgrammingError
    if database already exists.
    Warning: MySQL charset utf8mb4 will not allow adding unique index to
    peewee's CharField.
    :return:
    """
    con = msdb.connect(**_config)
    cursor = con.cursor()
    sql = "CREATE DATABASE " + config.database['db']
    sql += " CHARSET = utf8 COLLATE = utf8_bin"
    try:
        cursor.execute(sql)
    except msdb.ProgrammingError, e:
        print e
    finally:
        con.close()


def drop_tables():
    """
    Drops tables: articles, categories, and mappingtable
    :return: None
    """
    db.connect()
    db.drop_tables([Article, Category, MappingTable, Word, WordFreq])
    db.close()

def make_tables_unicode():
    db = msdb.connect(**config.database)
    cursor = db.cursor()
    db_name = config.database['db']
    sql_alter = "ALTER DATABASE {0}".format(db_name) + \
                "CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'"
    sql_select = "SELECT DISTINCT(table_name) FROM information_schema" + \
                 ".columns WHERE table_schema = '{0}'".format(db_name)
    cursor.execute(sql_alter)
    cursor.execute(sql_select)
    results = cursor.fetchall()
    for table in results:
        sql = "ALTER TABLE {0} convert to character set".format(table[0]) + \
              "DEFAULT COLLATE DEFAULT"
        cursor.execute(sql)
    db.close()