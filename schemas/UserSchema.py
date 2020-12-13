from flask_login import UserMixin
from marshmallow_mongoengine import ModelSchema

from ..models.UserModel import User


class UserSchema(ModelSchema):
    class Meta:
        model = User
        model_fields_kwargs = {'password': {'load_only': True},'_id':{'dump_only':True},'exclude':{'user_dict'}}
        model_build_obj = False





