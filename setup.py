from setuptools import setup

setup(
    name="corenlp-xml",
    version="1.0.3",
    author="Robert Elwell",
    author_email="robert.elwell@gmail.com",
    description="Library for interacting with the XML output of the Stanford CoreNLP pipeline.",
    url="https://github.com/relwell/corenlp-xml-lib",
    license="Other",
    packages=["corenlp_xml"],
    install_requires=["PyYAML>=3.10", "bidict>=0.1.1", "lxml>=3.2.4", "nltk>=2.0.4"]
    )
