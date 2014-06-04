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
        :rtype: Mention
        
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
        :return: the sentence this mention relates to
        :rtype: corenlp_xml.document.Sentence

        """
        if self._sentence is None:
            sentences = self._element.xpath('sentence/text()')
            if len(sentences) > 0:
                self._sentence = self._coref.document.get_sentence_by_id(int(sentences[0]))
        return self._sentence

    @property
    def siblings(self):
        """
        :return: the other mentions for this coref group
        :rtype: list
        """
        return [mention for mention in self._coref.mentions if mention is not self]

    @property
    def tokens(self):
        """
        :return: a list of tokens relating to this sentence
        :rtype: list
        """
        return self.sentence.tokens[self._start-1:self._end-1]

    @property
    def head(self):
        """
        :return: the token corresponding to the head
        :rtype: corenlp_xml.document.Token
        """
        if self._head is None:
            self._head = self.sentence.tokens[self._head_id]
        return self._head

    @property
    def representative(self):
        """
        Interprets and normalizes the "representative" attribute"
        """
        return self._element.get('representative', False) == 'true'
