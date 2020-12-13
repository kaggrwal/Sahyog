from datetime import datetime

from flask_login import UserMixin
from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField


class User(UserMixin,Document):
    email = StringField(required=True,unique=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50)
    phone_number = StringField(max_length=10)
    password = StringField(required=True)
    address = StringField(required=True)
    last_updated = DateTimeField(default=datetime.utcnow)
    user_type = StringField(required=True)
    user_dict = StringField(required=False)
    meta = {'indexes': [{'fields': ['$email']}],
            'allow_inheritance': True,"db_alias":"default",'collection':'user'}

    def get_id(self):
        object_id = self.user_dict['id']
        return str(object_id)



class Donor(User):
    #is_active = BooleanField(default=True)
    subscribtion_active = BooleanField(default=True)



