from setuptools import setup

setup(
    name="corenlp-xml-lib",
    version= "0.0.1",
    author = "Robert Elwell",
    author_email = "robert.elwell@gmail.com",
    description = "Library for interacting with the XML output of the Stanford CoreNLP pipeline.",
    license = "Other",
    packages = ["corenlp_xml"],
    depends = ["lxml"]
    )