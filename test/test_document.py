import os
import sys
sys.path.insert(0, os.path.join(".."))

import unittest
from corenlp_xml.document import Document, Sentence, Token
from collections import OrderedDict


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
        self.assertIsInstance(self._document._sentences, OrderedDict, "Protected sentences should be ordered")


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

    def test_tokens(self):
        self.assertIsNone(self._sentence._tokens, "Tokens should be lazy-loaded")
        self.assertGreater(len(self._sentence.tokens), 0, "Tokens should be generated")
        for token in self._sentence.tokens:
            self.assertIsInstance(token, Token, "Tokens should all be of class Token")
        self.assertIsNotNone(self._sentence._tokens, "Tokens should be memoized")
        self.assertIsInstance(self._sentence._tokens, OrderedDict, "Protected tokens should be ordered")


class TestToken(unittest.TestCase):

    """ Tests the Token class """
    def setUp(self):
        """ It would probably be a good idea to look into Mock, eventually """
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())
            self._sentence = self._document.sentences[0]
            self._token = self._sentence.tokens[0]

    def test_id(self):
        """ Value isn't None because it's initialized when getting tokens from sent. Hence why mocks might be nice. """
        self.assertIsNotNone(self._token._id, "id property should be memoized")
        self.assertEquals(1, self._token.id)

    def test_word(self):
        self.assertIsNone(self._token._word, "Word should be lazy-loaded")
        # BREAKAGE WARNING: depends on the current state of xml file test.xml
        self.assertEquals("Taking", self._token.word, "Word should be string value of word")
        self.assertIsNotNone(self._token._word, "Word property should be memoized")

    def test_lemma(self):
        self.assertIsNone(self._token._lemma, "Lemma should be lazy-loaded")
        # BREAKAGE WARNING: depends on the current state of xml file test.xml
        self.assertEquals("take", self._token.lemma, "Word should be string value of word")
        self.assertIsNotNone(self._token._lemma, "Lemma property should be memoized")

    def test_character_offset_begin(self):
        self.assertIsNone(self._token._character_offset_begin, "Character offset being should be lazy-loaded")
        self.assertIsNotNone(self._token.character_offset_begin, "Character offset should be accessible")
        self.assertIsNotNone(self._token._character_offset_begin, "Character offset property should be memoized")

    def test_character_offset_end(self):
        self.assertIsNone(self._token._character_offset_end, "Character offset being should be lazy-loaded")
        self.assertIsNotNone(self._token.character_offset_end, "Character offset should be accessible")
        self.assertIsNotNone(self._token._character_offset_end, "Character offset property should be memoized")

    def test_pos(self):
        self.assertIsNone(self._token._pos, "POS should be lazy-loaded")
        # BREAKAGE WARNING: depends on the current state of xml file test.xml
        self.assertEquals("VBG", self._token.pos, "POS should be a POS, yo")
        self.assertIsNotNone(self._token._pos, "POS property should be memoized")

    def test_ner(self):
        self.assertIsNone(self._token._ner, "NER should be lazy-loaded")
        # BREAKAGE WARNING: depends on the current state of xml file test.xml
        self.assertEquals("O", self._token.ner, "NER should be a NER, yo")
        self.assertIsNotNone(self._token._ner, "NER property should be memoized")

    def test_speaker(self):
        self.assertIsNone(self._token._speaker, "Speaker should be lazy-loaded")
        # BREAKAGE WARNING: depends on the current state of xml file test.xml
        self.assertEquals("PER0", self._token.speaker, "Speaker should be a speaker son")
        self.assertIsNotNone(self._token._speaker, "speaker property should be memoized")


def suite():
    """
    Generates test suite
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDocument))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSentence))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestToken))
    return test_suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())