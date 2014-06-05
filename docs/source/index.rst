.. CoreNLP XML Library documentation master file, created by
   sphinx-quickstart on Wed Jun  4 14:24:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CoreNLP XML Library's documentation!
===============================================

This library is designed to add a data model over Stanford CoreNLP's basic XML output.

The Document class is designed to provide lazy-loaded access to information
from syntax, coreference, and dependency parse structures within the XML.



Installing the Library
----------------------

It's as easy as 

.. code-block:: bash

   pip install corenlp_xml


What You Can Do With This Library
---------------------------------
Some code examples:

.. code-block:: python

   from corenlp_xml import Document
   
   doc = Document(xml_string)

   # The first sentence
   s1 = doc.sentences[0]

   # Noun phrases for the first sentence
   s1_nps = s1.phrase_strings("np")

   # Text of semantic head of first sentence
   s1_head = s1.semantic_head.text

   # Find all representative coreferences matching noun phrases in sentence 1
   s1_corefs = [coref for coref in doc.coreferences
                if coref.representative and coref.sentence == s1]



Contents:

.. toctree::
   :maxdepth: 2

   document
   dependencies
   coreference



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

