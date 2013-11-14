"""
Sub-module for handling document-level stuff
"""
from lxml import etree
from collections import OrderedDict
from nltk import Tree


class Document:
    """
    This class abstracts a Stanford CoreNLP Document
    """

    _sentences_dict = None
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

    @property
    def sentiment(self):
        """
        Returns average sentiment of document.
        :return: average sentiment of the document
        :rtype: float
        """
        if self._sentiment is None:
            results = self._xml.xpath('/root/document/sentences')
            self._sentiment = float(results[0].get("averageSentiment")) if len(results) > 0 else None
        return self._sentiment

    def _get_sentences_dict(self):
        """
        Returns sentence objects
        :return: order dict of sentences
        :rtype:class:`OrderedDict`
        """
        if self._sentences_dict is None:
            sentences = [Sentence(element) for element in self._xml.xpath('/root/document/sentences/sentence')]
            self._sentences_dict = OrderedDict([(s.id, s) for s in sentences])
        return self._sentences_dict

    @property
    def sentences(self):
        """
        Returns the ordered dict of sentences as a list.
        :return: list of sentences, in order
        :rtype:list
        """
        return self._get_sentences_dict().values()

    def get_sentence_by_id(self, id):
        """
        :param id: the ID of the sentence, as defined in the XML
        :type id: int
        :return:class:`Sentence`
        """
        return self._get_sentences_dict().get(id)


class Sentence():
    """
    This abstracts a sentence
    """
    _id = None
    _sentiment = None
    _tokens_dict = None
    _element = None
    _parse = None
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

    @property
    def id(self):
        """
        :return: the ID attribute of the sentence
        :rtype id: int
        """
        if self._id is None:
            self._id = int(self._element.get('id'))
        return self._id

    @property
    def sentiment(self):
        """
        :return: the sentiment value of this sentence
        :rtype int:
        """
        if self._sentiment is None:
            self._sentiment = int(self._element.get('sentiment'))
        return self._sentiment

    def _get_tokens_dict(self):
        """
        :return: The ordered dict of the tokens
        :rtype:class:`OrderedDict`
        """
        if self._tokens_dict is None:
            tokens = [Token(element) for element in self._element.xpath('tokens/token')]
            self._tokens_dict = OrderedDict([(t.id, t) for t in tokens])
        return self._tokens_dict

    @property
    def tokens(self):
        """
        :return: a list of Token instances
        :rtype:list
        """
        return self._get_tokens_dict().values()

    def get_token_by_id(self, id):
        """
        :param id: The XML ID of the token
        :type id: int
        :return: The token
        :rtype:class:`Token`
        """
        return self._get_tokens_dict().get(id)

    @property
    def parse(self):
        """
        :return: The NLTK parse tree
        :rtype:class:`nltk.Tree`
        """
        if self._parse is None:
            self._parse = Tree.parse(self._parse)
        return self._parse


class Token():
    """
    Wraps the token XML element
    """

    _id = None
    _word = None
    _lemma = None
    _character_offset_begin = None
    _character_offset_end = None
    _pos = None
    _ner = None
    _speaker = None
    _element = None

    def __init__(self, element):
        """
        Constructor method
        :param element: An etree element
        :type element:class:`lxml.etree.ElementBase`
        """
        self._element = element

    @property
    def id(self):
        """
        Lazy-loads ID
        :return: The ID of the token element
        :rtype: int
        """
        if self._id is None:
            self._id = int(self._element.get('id'))
        return self._id

    @property
    def word(self):
        """
        Lazy-loads word value
        :return: The plain string value of the word
        :rtype: str
        """
        if self._word is None:
            words = self._element.xpath('word/text()')
            if len(words) > 0:
                self._word = words[0]
        return self._word

    @property
    def lemma(self):
        """
        Lazy-loads the lemma for this word
        :return: The plain string value of the word lemma
        :rtype: str
        """
        if self._lemma is None:
            lemmata = self._element.xpath('lemma/text()')
            if len(lemmata) > 0:
                self._lemma = lemmata[0]
        return self._lemma

    @property
    def character_offset_begin(self):
        """
        Lazy-loads character offset begin node
        :return: the integer value of the offset
        :rtype: int
        """
        if self._character_offset_begin is None:
            offsets = self._element.xpath('CharacterOffsetBegin/text()')
            if len(offsets) > 0:
                self._character_offset_begin = int(offsets[0])
        return self._character_offset_begin

    @property
    def character_offset_end(self):
        """
        Lazy-loads character offset end node
        :return: the integer value of the offset
        :rtype: int
        """
        if self._character_offset_end is None:
            offsets = self._element.xpath('CharacterOffsetEnd/text()')
            if len(offsets) > 0:
                self._character_offset_end = int(offsets[0])
        return self._character_offset_end

    @property
    def pos(self):
        """
        Lazy-loads the part of speech tag for this word
        :return: The plain string value of the POS tag for the word
        :rtype: str
        """
        if self._pos is None:
            poses = self._element.xpath('POS/text()')
            if len(poses) > 0:
                self._pos = poses[0]
        return self._pos

    @property
    def ner(self):
        """
        Lazy-loads the NER for this word
        :return: The plain string value of the NER tag for the word
        :rtype: str
        """
        if self._ner is None:
            ners = self._element.xpath('NER/text()')
            if len(ners) > 0:
                self._ner = ners[0]
        return self._ner

    @property
    def speaker(self):
        """
        Lazy-loads the speaker for this word
        :return: The plain string value of the speaker tag for the word
        :rtype: str
        """
        if self._speaker is None:
            speakers = self._element.xpath('Speaker/text()')
            if len(speakers) > 0:
                self._speaker = speakers[0]
        return self._speaker


