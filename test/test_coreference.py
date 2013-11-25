import os
import sys
sys.path.insert(0, os.path.join(".."))

import unittest
from corenlp_xml.document import Document, Sentence, TokenList, Token
from corenlp_xml.coreference import *


class TestCoreference(unittest.TestCase):

    def setUp(self):
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())

    def test_coreferences_lazyload(self):
        self.assertIsNone(self._document._coreferences, "Document should lazy-load coreferences")
        self.assertIsInstance(self._document.coreferences[0], Coreference, "Document should lazy-load coreferences")
        self.assertIsInstance(self._document._coreferences[0], Coreference, "Document should memoize coreferences")

    def test_coreference_mentions_lazyload(self):
        self.assertIsNone(self._document.coreferences[0]._mentions, "Mentions should be lazy-loaded")
        self.assertIsInstance(self._document.coreferences[0].mentions[0], Mention, "Mention should be lazy loaded")
        self.assertIsInstance(self._document.coreferences[0]._mentions[0], Mention, "Mentions should be memoized")

    def test_coreference_representative_lazyload(self):
        coref = self._document.coreferences[0]
        self.assertIsNone(coref._representative, "Representative should be lazy-loaded")
        self.assertIsNone(coref._mentions, "Mentions should be lazy-loaded")
        self.assertIsInstance(coref.representative, Mention, "Representative mention should be lazy-loaded")
        self.assertIsInstance(coref._representative, Mention, "Representative mention should be memoized")
        self.assertIsInstance(coref._mentions[0], Mention, "Mentions should be lazy-loaded and memoized too")


class TestMention(unittest.TestCase):

    def setUp(self):
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())
            self._coref = self._document.coreferences[0]
            self._mention = self._coref.mentions[0]

    def test_sentence(self):
        self.assertIsNone(self._mention._sentence, "Sentence should be lazy-loaded")
        self.assertIsInstance(self._mention.sentence, Sentence, "Sentence should be lazy-loaded")
        self.assertIsInstance(self._mention._sentence, Sentence, "Sentence should be lazy-loaded")

    def test_siblings(self):
        self.assertTrue(len(self._mention.siblings) == len(self._document.coreferences[0].mentions) - 1,
                        "Siblings should be a list of mentions not including this mention")

    def test_tokens(self):
        self.assertIsNone(self._mention._sentence, "Sentence should be lazy-loaded")
        self.assertIsInstance(self._mention.tokens, TokenList, "Return value should be TokenList")
        self.assertIsInstance(self._mention._sentence, Sentence, "Sentence should be memoized")
        self.assertEquals("Pixar 's", str(self._mention.tokens),
                          "Token list should match up to mention, even with numbering weirdness")

    def test_head(self):
        self.assertIsNone(self._mention._head, "Head should be lazy-loaded")
        self.assertIsInstance(self._mention.head, Token, "Head should be a token")
        self.assertIsInstance(self._mention._head, Token, "Head should be memoized")

    def test_representative(self):
        self.assertEquals(len([m for m in self._coref.mentions if m.representative]), 1,
                          "Should be only one representative")


def suite():
    """
    Generates test suite
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCoreference))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMention))
    return test_suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())