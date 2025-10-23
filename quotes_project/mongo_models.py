from mongoengine import Document, CASCADE
from mongoengine.fields import StringField, ListField, ReferenceField, BooleanField, EmailField


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(required=True, unique=True)
    meta = {'collection': 'quotes'}


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone_number = StringField()
    message_sent = BooleanField(default=False)
    preferred_method = StringField(choices=('email', 'sms'), default='email')
    meta = {'collection': 'contacts'}
