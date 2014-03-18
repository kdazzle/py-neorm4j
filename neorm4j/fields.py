class Field(object):
    pass


class Property(Field):

    def __init__(self, index=False, *args, **kwargs):
        """
        :param index: set to True if you want the Property to be an index.
            Defaults to false.
        """
        self.index = index

    def is_index(self):
        """
        Is this property field an index?

        :return: Boolean
        """
        return self.index

    @staticmethod
    def save_properties(node, properties):
        """
        Adds multiple properties to the given node

        :param node: a Neo4j node
        :param properties: a dictionary of property names to values.
                For example: {'id': 10}
        """
        for property_name, value in properties.iteritems():
            node[property_name] = value


class RelationshipField(Field):
    """
    The base class for a relationship field.

    In the owning class, declare a relationship like:
        RelationshipTo('OtherClassName', 'relationship_description')

    with the first argument, 'OtherClassName', being the name of the class that
    the field will relate with (which isn't enforced right now). The second
    argument, 'relationship_description', is just a pithy string summarizing
    the relationship.

    For example, Person "knows" another Person can be written like:
        class Person(Node):

            friend = RelationshipTo('Person', "knows")
    """

    def __init__(self, relation, relationship_type, *args, **kwargs):
        """
        :param relation: the Node that has a relationship with this Node
        :param relationship_type: a pithy string summarizing the relationship
                        for example: "Knows"
        """
        self.relationship_type = relationship_type
        self.relation = relation

    @staticmethod
    def save_relationships(instance, node, relationships):
        """
        :param instance: the instance that contains this relationship field
        :param node: the start node of a directional relationship
            :type node: neo4jrestclient.client.Node
        :param relationships: a dictionary of attribute names to their values:
                {"vector": VectorObj}
        """
        calling_class = instance.__class__

        for attribute_name, related_node in relationships.iteritems():
            relationship_field = getattr(calling_class, attribute_name)
            relationship_type = relationship_field.relationship_type
            relationship_field.save_relationship(node, related_node,
                                                 relationship_type)


class RelationshipTo(RelationshipField):
    """
    For a relationship between the node that owns this property as the start
    node and another as the ending node.

        See the documentation for RelationshipField
    """

    @staticmethod
    def save_relationship(start_node, end_node, relationship_type):
        start_node.relationships.create(relationship_type, end_node)


class RelationshipFrom(RelationshipField):
    """
    For a relationship with the arrow of directionality pointing away from
    the owning node

        See the documentation for RelationshipField
    """

    @staticmethod
    def save_relationship(end_node, start_node, relationship_type):
        start_node.neo4j_node.relationships.create(relationship_type, end_node)
