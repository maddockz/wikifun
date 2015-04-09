__author__ = 'maddockz'

import wikifun.model.idiots_bayes as ib

class TestDataPreprocessing:
    def setup(self):
        pass

    def test_make_X(self):
        X = ib.make_X(ib.train[0:3])
        assert X.shape[0] == 3, X.shape[0]
