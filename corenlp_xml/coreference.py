"""
This library is responsible for handling coreference resolution parsing from the XML output
"""


class Coreference():
    """
    Reflects a grouping of mentions
    """

    def __init__(self, document, element):
        """
        Constructor method

        :param document: the document handling these relationships
        :type document: corenlp_xml.document.Document
        :param element: an lxml element
        :type element: lxml.etree.ElementBase

        """
        self._element = element
        self._mentions = None
        self._representative = None
        self.document = document

    @property
    def mentions(self):
        """
        Returns mentions

        :return: list of mentions
        :rtype: list

        """
        if self._mentions is None:
            self._mentions = []
            for mention_element in self._element.xpath('mention'):
                this_mention = Mention(self, mention_element)
                self._mentions.append(this_mention)
                if this_mention.representative:
                    self._representative = this_mention
        return self._mentions

    @property
    def representative(self):
        """
        Representative mention

        :return: representative Mention
        :rtype: corenlp_xml.coreference.Mention
        
        """
        if self._representative is None:
            """ Lazy-loaded! """
            self.mentions
        return self._representative


class Mention():
    """
    Reflects a given mention
    """

    def __init__(self, coref, element):
        """
        Constructor method
        
        :param coref: a coreference grouping
        :type coref: corenlp_xml.coreference.Coreference
        :param element: an xml element
        :type element: lxml.etree.ElementBase
        
        """
        self._coref = coref
        self._element = element
        self._start = int(element.xpath('start/text()')[0])
        self._end = int(element.xpath('end/text()')[0])
        self._sentence_id = int(element.xpath('sentence/text()')[0])
        self._sentence = None
        self._head_id = int(element.xpath('head/text()')[0])
        self._head = None
        texts = element.xpath('text/text()')
        self.text = texts[0] if len(texts) > 0 else ''  # one-off bug?

    @property
    def sentence(self):
        """
        The sentence related to this mention

        :getter: returns the sentence this mention relates to
        :type: corenlp_xml.document.Sentence

        """
        if self._sentence is None:
            sentences = self._element.xpath('sentence/text()')
            if len(sentences) > 0:
                self._sentence = self._coref.document.get_sentence_by_id(int(sentences[0]))
        return self._sentence

    @property
    def siblings(self):
        """
        Accesses other mentions in this coref group

        :getter: the other mentions for this coref group
        :type: list of corenlp_xml.coreference.Mention

        """
        return [mention for mention in self._coref.mentions if mention is not self]

    @property
    def tokens(self):
        """
        A list of tokens related to this mention

        :getter: returns a list of tokens relating to this mention
        :type: list of corenlp_xml.document.Token

        """
        return self.sentence.tokens[self._start-1:self._end-1]

    @property
    def head(self):
        """
        The token serving as the "head" of the mention

        :getter: the token corresponding to the head
        :type: corenlp_xml.document.Token

        """
        if self._head is None:
            self._head = self.sentence.tokens[self._head_id]
        return self._head

    @property
    def representative(self):
        """
        Interprets and normalizes the "representative" attribute"

        :getter: determines whether the mention is representative
        :type: bool

        """
        return self._element.get('representative', False) == 'true'
