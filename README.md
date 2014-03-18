py-neorm4j
==========

A basic ORM for Neo4j in Python


##About

The library is very basic right now, but is based off of Django's ORM.


##Connecting to your Database

In neorm4j.__init__, set db to whatever the URL might be as specified in
https://neo4j-rest-client.readthedocs.org/en/latest/#getting-started


##Creating Objects

Just import the Node class from neorm4j.models for the objects themselves, and
for fields, check out neorm4j.fields.

The field types are:
* Property - for basic properties of any type. These are indexable.
* RelationshipTo - For a relationship between the owning node as the start node
and another as the ending node. Relationships are not indexable yet.
* RelationshipFrom - Like RelationshipTo, except with the arrow pointing at
the Node owning that field.

```python
from neorm4j.models import Node
from neorm4j.fields import Property, RelationshipTo


class Person(Node):

    id = Property(index=True)
    hobby = Property()
    friend = RelationshipTo("Person", "knows")


adam = Person(id=1)
adam.hobby = 'Drums'
adam.save()

eve = Person(id=2, hobby='Studying Nietzsche')
eve.friend = adam
eve.save()
```

Adam and Eve will both be created as nodes in the database, indexed by id, and
labeled by their class, Person.
