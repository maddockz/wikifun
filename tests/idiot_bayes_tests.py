__author__ = 'maddockz'

import numpy as np

import wikifun.model.idiots_bayes as ib
import wikifun.etl.data_models as dm
import wikifun.etl.word_count as wc

class TestDataPreprocessing:
    def setup(self):
        self.article = ib.train[0]

    def test_make_X_basic(self):
        X = ib.make_X([self.article])
        assert X.shape[0] == 1, X.shape[0]
        word_count = np.sum(wc.count(self.article.text).values())
        assert np.abs( np.sum(X.todense()) - word_count ) < 10

    def test_make_y_basic(self):
        assert ib.make_y([self.article])[0] == False
