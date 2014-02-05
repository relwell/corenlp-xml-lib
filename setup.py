from setuptools import setup

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="corenlp-xml-lib",
    version="0.0.1",
    author="Robert Elwell",
    author_email="robert.elwell@gmail.com",
    description="Library for interacting with the XML output of the Stanford CoreNLP pipeline.",
    license="Other",
    packages=["corenlp_xml"],
    install_requires=reqs
    )