"""
Data models for wikipedia articles
"""
__author__ = 'maddockz'

import peewee as pw
import MySQLdb as msdb
import config

__config = {key: config.database[key] for key in filter(lambda x: x is not 'db',
                                                        config.database.keys())}
try:
    db = pw.MySQLDatabase(config.database['db'], **__config)
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
    is_history = pw.BooleanField(null=True)
    is_sports = pw.BooleanField(null=True)


class Category(BaseModel):
    value = pw.CharField(unique=True, null=False)


class MappingTable(BaseModel):
    article = pw.ForeignKeyField(Article)
    category = pw.ForeignKeyField(Category)


def create_tables():
    """
    Creates tables articles, categories, and mappingtable if do not exist
    :return: None
    """
    db.connect()
    for model in [Article, Category, MappingTable]:
        try:
            model.create_table()
        except pw.OperationalError, err:
            "Table {0} already exists".format(str(model))

    db.close()

def drop_tables():
    """
    Drops tables: articles, categories, and mappingtable
    :return: None
    """
    db.connect()
    db.drop_tables([Article, Category, MappingTable])
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