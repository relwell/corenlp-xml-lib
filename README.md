Data abstraction library for Stanford CoreNLP XML parses.

Using it is as easy as:

    from corenlp_xml import Document
    d = Document(corenlp_xml_output_string)
    sentences = d.sentences
    word_to_pos = dict([(token.word, token.pos) for token in sentences[0].tokens])
    
To learn more:
    
 * [Documentation on ReadTheDocs](http://corenlp-xml-library.readthedocs.org/en/latest/index.html)
 * [pypi](https://pypi.python.org/pypi/corenlp-xml/0.0.1)
