__author__ = 'maddockz'

import wikifun.etl.word_count as wc
import wikifun.etl.data_models as dm

class TestWordCounts:
    def setUp(self):
        self.text="""
                The word A is written twice A?
                Word appears twice?
                Twice appears thrice.
                Appears[appears] as well.
                """
        self.anarchy = dm.Article.get(dm.Article.title == 'Anarchism')

    def test_basic_count(self):
        freqs = wc.count(self.text)
        assert freqs['a'] == 2
        assert freqs['twice'] == 3
        assert freqs['appears'] == 4
        assert freqs['Twice'] == 0

    def test_anarchy_count(self):
        freqs = wc.count(self.anarchy.text)
        assert freqs['absurdity'] == 1
        assert None not in freqs.keys()

    def test_anarchy_database_count(self):
        # Test that 'Anarchy' article stored in database
        # has frequency stored for 'absurdity' equal to 1.
        absurd = dm.Word.get(dm.Word.value == "absurdity")
        wf = dm.WordFreq.get(dm.WordFreq.article == self.anarchy,
                             dm.WordFreq.word == absurd)
        assert wf.freq == 1



