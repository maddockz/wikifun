__author__ = 'maddockz'

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
