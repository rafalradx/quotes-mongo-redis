from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import (
    EmbeddedDocumentField,
    ListField,
    StringField,
    ReferenceField,
)


class Tag(EmbeddedDocument):
    name = StringField()


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    quote = StringField()
    author = ReferenceField(Author)
    tags = ListField(EmbeddedDocumentField(Tag))
