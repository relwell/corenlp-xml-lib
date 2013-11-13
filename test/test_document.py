import os
import sys
sys.path.insert(0, os.path.join(".."))

import unittest
from corenlp_xml.document import Document, Sentence


class TestDocument(unittest.TestCase):

    def setUp(self):
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())

    def test_sentiment(self):
        self.assertIsNone(self._document._sentiment, "Sentiment should be lazy-loaded")
        expected = 1.2173913043478262
        self.assertEquals(expected, self._document.get_sentiment(), "Sentiment should be returned upon invocation")
        self.assertEquals(expected, self._document._sentiment, "Sentiment should be memoized")
        self.assertEquals(expected, self._document.sentiment, "Sentiment property should return same value as call")

    def test_sentences(self):
        self.assertIsNone(self._document._sentences, "Sentences should be lazy-loaded")
        sentences = self._document.get_sentences()
        self.assertGreater(len(sentences), 0, "We should have sentences")
        for sentence in sentences:
            self.assertIsInstance(sentence, Sentence, "Sentences should be a list of only sentences")
        self.assertEquals(self._document.sentences, sentences, "Sentences property should work")


def suite():
    """
    Generates test suite
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDocument))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())