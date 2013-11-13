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
        self.assertEquals(expected, self._document._get_sentiment(), "Sentiment should be returned upon invocation")
        self.assertIsNotNone(self._document._sentiment, "Sentiment should be memoized")
        self.assertEquals(expected, self._document._sentiment, "Sentiment should be memoized")
        self.assertEquals(expected, self._document.sentiment, "Sentiment property should return same value as call")

    def test_sentences(self):
        self.assertIsNone(self._document._sentences, "Sentences should be lazy-loaded")
        sentences = self._document._get_sentences()
        self.assertIsNotNone(self._document._sentences, "Sentences should be memoized")
        self.assertGreater(len(sentences), 0, "We should have sentences")
        for sentence in sentences:
            self.assertIsInstance(sentence, Sentence, "Sentences should be a list of only sentences")
        self.assertEquals(self._document.sentences, sentences, "Sentences property should work")


class TestSentence(unittest.TestCase):

    """ Tests the Sentence class """

    def setUp(self):
        """ It would probably be a good idea to look into Mock, eventually """
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())
            self._sentence = self._document.sentences[0]

    def test_id(self):
        """ Value isn't None because it's initialized when you create a Document. Hence why mocks might be nice. """
        self.assertEquals(1, self._sentence._get_id())
        self.assertIsNotNone(self._sentence._id, "id property should be memoized")
        self.assertEquals(1, self._sentence.id)

    def test_sentiment(self):
        self.assertIsNone(self._sentence._sentiment, "Sentiment should be lazy-loaded")
        self.assertEquals(1, self._sentence.sentiment, "Sentiment should be an int")


def suite():
    """
    Generates test suite
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDocument))
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())