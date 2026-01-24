from mongoengine import Document,StringField,ListField,ReferenceField
class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    meta = {"collection": "authors",
            "auto_create_index": False}

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)

    meta = {"collection": "quotes",
            "auto_create_index":False}
