"""
Submodule for handling document-level stuff
"""
from lxml import etree


class Document:
    """
    This class abstracts a Stanford CoreNLP Document
    """

    _sentences = None
    _sentiment = None
    _xml_string = None
    _xml = None

    def __init__(self, xml_string):
        """
        Constructor method.
        :param xml_string: The XML string we're going to parse and represent, coming from CoreNLP
        :type xml_string: str
        """
        self._xml_string = xml_string
        self._xml = etree.fromstring(xml_string)

    def get_sentiment(self):
        """
        Returns average sentiment of document.
        """
        if self._sentiment is None:
            results = self._xml.xpath('/root/document/sentences')
            self._sentiment = float(results[0].get("averageSentiment")) if len(results) > 0 else None
        return self._sentiment
    sentiment = property(get_sentiment)

    def get_sentences(self):
        """
        Returns sentence objects
        """
        if self._sentences is None:
            sentences = [Sentence(element) for element in self._xml.xpath('/root/document/sentences/sentence')]
            self._sentences = dict([(s.get_id(), s) for s in sentences])
        return self._sentences.values()
    sentences = property(get_sentences)


class Sentence():
    """
    This abstracts a sentence
    """
    _id = None
    _sentiment = None
    _tokens = None
    _element = None
    _basic_dependencies = None
    _collapsed_dependencies = None
    _collapsed_ccprocessed_dependencies = None

    def __init__(self, element):
        """
        Constructor method
        :param element: An etree element.
        :type element:class:`lxml.etree.ElementBase`
        """
        self._element = element

    def get_id(self):
        """
        :return: the ID attribute of the sentence
        :rtype id: int
        """
        if self._id is None:
            self._id = int(self._element.get('id'))
        return self._id
    id = property(get_id)

    def get_sentiment(self):
        """
        :return: the sentiment value of this sentence
        :rtype int:
        """
        if self._sentiment is None:
            self._sentiment = int(self._element.get('sentiment'))
        return self._sentiment
    sentiment = property(get_sentiment)

    def get_tokens(self):
        """
        :return: a list of Token instances
        :rtype: list
        """
        if self._tokens is None:
            tokens = [Token(element) for element in self._element.iterfind('token')]
            self._tokens = dict([(int(t.get('id')), t) for t in tokens])
        return self._tokens
    tokens = property(get_tokens)


class Token():
    """
    Wraps the token XML element
    """

    word = None
    lemma = None
    character_offset_begin = None
    character_offset_end = None
    pos = None
    ner = None
    speaker = None

    def __init__(self, element):
        """
        Constructor method
        :param element: An etree element
        :type element:class:`lxml.etree.ElementBase`
        """
        self.element = element