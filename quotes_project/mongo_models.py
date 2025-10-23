from mongoengine import Document, StringField, ListField, ReferenceField


class Author(Document):
    fullname = StringField(required=True, unique=True, max_length=150)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()

    meta = {
        'collection': 'authors'
    }


class Quote(Document):
    quote = StringField(required=True)
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, required=True)

    meta = {
        'collection': 'quotes'
    }
