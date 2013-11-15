import os
import sys
sys.path.insert(0, os.path.join(".."))

import unittest
from corenlp_xml.document import Document
from corenlp_xml.dependencies import *


class TestDependencyGraph(unittest.TestCase):

    def setUp(self):
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())
            self._graph = self._document.sentences[0].basic_dependencies

    def test_nodes(self):
        self.assertIsInstance(self._graph.get_node_by_idx(1),
                              DependencyNode,
                              "A node should be accessible within the graph by its idx")
        self.assertIsNone(self._graph.get_node_by_idx(-1),
                          "A non-existent node idx should result in None")

    def test_links(self):
        for link in self._graph.links:
            self.assertIsInstance(link, DependencyLink, "links should only be DependencyLink instances")
        self.assertGreater(len(self._graph.links_by_type('prep')),
                           0,
                           "You should be able to filter dependencies by type using kwargs")


class TestDependencyLink(unittest.TestCase):

    def setUp(self):
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())
            self._graph = self._document.sentences[0].basic_dependencies
            self._link = self._graph.links_by_type('root')[0]

    def test_governor(self):
        self.assertIsInstance(self._link.governor, DependencyNode)

    def test_dependent(self):
        self.assertIsInstance(self._link.dependent, DependencyNode)


class TestDependencyNode(unittest.TestCase):

    def setUp(self):
        with open("test.xml", "r") as xml_file:
            self._document = Document(xml_file.read())
            self._graph = self._document.sentences[0].basic_dependencies
            self._link = self._graph.links_by_type('root')[0]
            self._node = self._link.governor

    def test_load(self):
        # gonna need mocking for this
        pass

    def test_dependents_and_governors(self):
        for dep in self._node.dependents:
            self.assertIsInstance(dep,
                                  DependencyNode,
                                  "Dependents should only be DependencyNode instances")

            self.assertIn(dep,
                          self._node.dependents_by_type(self._link.type),
                          "This dependency should be registered by type")

            self.assertIn(self._node,
                          dep.governors,
                          "Governor should be registered in dependent node")

            self.assertIn(self._node,
                          dep.governors_by_type(self._link.type),
                          "This dependency should be registered by type")


def suite():
    """
    Generates test suite
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDependencyGraph))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDependencyLink))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDependencyNode))
    return test_suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())