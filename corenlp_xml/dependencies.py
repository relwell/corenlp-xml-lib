"""
This component is responsible for managing dependency parses
"""


class DependencyGraph():
    """
    Dependency graph, models a dependency parse
    """

    def __init__(self, element):
        """
        Constructor method

        :param element: An lxml element
        :type element: class:lxml.etree.ElementBase

        """
        self._element = element
        self.type = element.get('type')
        self._nodes = dict()
        self._links_by_type = dict()
        for dep in self._element.xpath('dep'):
            link = DependencyLink(self, dep)
            self._links_by_type[link.type] = self._links_by_type.get(link.type, []) + [link]

    def get_node_by_idx(self, idx):
        """
        Stores each distinct node in a dict

        :param idx: the "idx" value of the node
        :type idx: int

        :return: the node instance for that index
        :type: corenlp_xml.dependencies.DependencyNode

        """
        return self._nodes.get(int(idx))

    @property
    def links(self):
        """
        Accesses links within the graph

        :return: a list of corenlp_xml.dependencies.DependencyLink instances
        :type: list of corenlp_xml.dependencies.DependencyLink

        """
        return [link for grouping in self._links_by_type.values() for link in grouping]

    def links_by_type(self, dep_type):
        """
        Accesses links within the graph

        :param dep_type: the depency type
        :type dep_type: str

        :return: a list of corenlp_xml.dependencies.DependencyLink instances
        :type: list of corenlp_xml.dependencies.DependencyLink

        """
        return self._links_by_type.get(dep_type, [])

    def register_node(self, node):
        self._nodes[node.idx] = node


class DependencyNode():
    """
    Represents a node in a dependency graph
    """

    def __init__(self, graph, element):
        """
        Instantiates the node in the graph

        :param graph: The dependency graph this node is a member of
        :type graph: corenlp_xml.dependencies.DependencyGraph
        :param element: The lxml element wrapping the node
        :type element: lxml.ElementBase

        """
        self._graph = graph
        self.idx = int(element.get('idx'))
        self.text = element.text
        """
        These properties are dicts of link type to node
        """
        self._governors = dict()
        self._dependents = dict()

    @classmethod
    def load(cls, graph, element):
        """
        Instantiates the node in the graph if it's not already stored in the graph

        :param graph: The dependency graph this node is a member of
        :type graph: corenlp_xml.dependencies.DependencyGraph
        :param element: The lxml element wrapping the node
        :type element: lxml.ElementBase

        """
        node = graph.get_node_by_idx(id(element.get("idx")))
        if node is None:
            node = cls(graph, element)
            graph.register_node(node)
        return node

    @property
    def governors(self):
        """
        Gets governing nodes

        :getter: returns a flat list of all governing nodes
        :type: list of corenlp_xml.dependencies.DependencyNode

        """
        return [value for grouping in self._governors.values() for value in grouping]

    @property
    def dependents(self):
        """
        Gets dependent nodes

        :getter: returns a flat list of all governing nodes
        :type: list of corenlp_xml.dependencies.DependencyNode

        """
        return [value for grouping in self._dependents.values() for value in grouping]

    def dependents_by_type(self, dep_type):
        """
        Gets the dependents of this node by a given dependency type

        :param dep_type: The dependency type
        :type dep_type: str

        :return: dependents matching the provided type

        """
        return self._dependents.get(dep_type, [])

    def governors_by_type(self, dep_type):
        """
        Gets the governors of this node filtered by a dependency type

        :param dep_type: The dependency type
        :type dep_type: str

        :return: governors matching the provided type

        """
        return self._governors.get(dep_type, [])

    def governor(self, dep_type, node):
        """
        Registers a node as governing this node

        :param dep_type: The dependency type
        :type dep_type: str
        :param node:

        :return: self, provides fluent interface
        :rtype: corenlp_xml.dependencies.DependencyNode

        """
        self._governors[dep_type] = self._governors.get(dep_type, []) + [node]
        return self

    def dependent(self, dep_type, node):
        """
        Registers a node as dependent on this node

        :param dep_type: The dependency type
        :type dep_type: str
        :param node: The node to be registered as a dependent
        :type node: corenlp_xml.dependencies.DependencyNode

        :return: self, provides fluent interface
        :rtype: corenlp_xml.dependencies.DependencyNode

        """
        self._dependents[dep_type] = self._dependents.get(dep_type, []) + [node]
        return self


class DependencyLink():
    """
    Represents a relationship between two nodes in a dependency graph
    """

    def __init__(self, graph, element):
        """
        Constructor method

        :param graph: The parent graph
        :type graph: corenlp_xml.dependencies.DependencyGraph
        :param element: An lxml element
        :type element: lxml.etree.ElementBase

        """
        self._graph = graph
        self._element = element
        self.type = element.get('type')
        self._dependent = None
        self._governor = None
        """
        Register relationship within nodes
        """
        self.dependent.governor(self.type, self.governor)
        self.governor.dependent(self.type, self.dependent)

    @property
    def governor(self):
        """
        Accesses the governor node

        :getter: Returns the Governor node
        :type: corenlp_xml.dependencies.DependencyNode

        """
        if self._governor is None:
            governors = self._element.xpath('governor')
            if len(governors) > 0:
                self._governor = DependencyNode.load(self._graph, governors[0])
        return self._governor

    @property
    def dependent(self):
        """
        Accesses the dependent node

        :getter: returns the Dependent node
        :type: corenlp_xml.dependencies.DependencyNode

        """
        if self._dependent is None:
            dependents = self._element.xpath('dependent')
            if len(dependents) > 0:
                self._dependent = DependencyNode.load(self._graph, dependents[0])
        return self._dependent