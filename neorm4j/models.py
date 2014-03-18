from neo4jrestclient.query import Q

from .__init__ import db
from .fields import Property, RelationshipFrom, RelationshipTo


class NodeManager(object):

    @staticmethod
    def find_by_property(property, value):
        """
        Performs a case-sensitive query on the database and returns
        matching nodes

        :param property: string - the property being queried
        :param value: the value that the property should be (case-sensitive)
        :return: list of nodes
        """
        lookup = Q(property, exact=value)
        return db.nodes.filter(lookup)


class Node(object):

    manager = NodeManager()

    @property
    def id(self):
        return self._get_neo4j_node_attr('id')

    @property
    def url(self):
        return self._get_neo4j_node_attr('url')

    def __init__(self, *args, **kwargs):
        self.neo4j_node = None

    def _get_neo4j_node_attr(self, attr_name):
        if self.neo4j_node:
            return getattr(self.neo4j_node, attr_name, None)

        return None

    @staticmethod
    def _add_property_index(index_name):
        """
        Create an index for a property in the database if it doesn't
        already exist.

        This method should probably not be in this class.

        :param index_name: the name of the index being created
        """
        existing_indexes = db.nodes.indexes
        if not index_name in existing_indexes:
            db.nodes.indexes.create(index_name)

    def save(self):
        """
        Save properties, relationships, and labels to the database.
        """
        #TODO: This should be in a transaction

        #TODO: Create or update
        self.neo4j_node = db.nodes.create()
        self.neo4j_node.labels.add(self.__class__.__name__)

        properties_by_class_name = self._get_fields_by_class()
        self._save_property_indexes(properties_by_class_name.get('Property', {}))
        self._save_fields(properties_by_class_name)

    def _save_property_indexes(self, properties):
        for property_name in properties:
            # Get the static property
            static_property = getattr(self.__class__, property_name)
            if static_property.is_index():
                Node._add_property_index(property_name)

    def _save_fields(self, properties_by_class_name):
        """
        Saves all of the properties and relationships of a node

        :param properties_by_class_name: see self._get_fields_by_class()
        """
        properties = properties_by_class_name.get('Property', {})
        relationship_to_properties = properties_by_class_name.get(
            'RelationshipTo', {})
        relationship_from_properties = properties_by_class_name.get(
            'RelationshipFrom', {})

        Property.save_properties(self.neo4j_node, properties)
        RelationshipTo.save_relationships(
            self, self.neo4j_node, relationship_to_properties)
        RelationshipFrom.save_relationships(
            self, self.neo4j_node, relationship_from_properties)

    def _get_fields_by_class(self):
        """
        Sorts attributes by their class.

        :return dict 2-dimensional dictionary mapped like:
            {'Property': {'id': 10} }
        """

        fields_by_class = {}

        for attribute_key, attribute_value in self.__dict__.iteritems():
            attribute = getattr(self.__class__, attribute_key, None)
            field_type = attribute.__class__.__name__

            fields_by_class.setdefault(field_type, {}).update({
                attribute_key: attribute_value
            })

        return fields_by_class
