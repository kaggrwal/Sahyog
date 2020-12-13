import pdb

from mongoengine import *
from nameko.rpc import rpc
from werkzeug.security import generate_password_hash, check_password_hash

from ..exceptions.GeneralExceptions import UserServiceException
from ..models.UserModel import Donor, User
from ..exceptions.UserServiceExceptions import UserNotFoundException
#from nameko_mongodb import MongoDatabase
from ..schemas.UserSchema import UserSchema


class UserService:
    name = "user_service"
    #db = MongoDatabase()
    connect('Sahyog', host='localhost', port=27017)


    @rpc
    def getUserByEmail(self, email):
        #self.db.list_collection_names()
        print(email)

        user = User.objects(email=email).first()
        #print(type(user))
        if user is not None:
            userSchema = UserSchema()
            userFecthed,errors = userSchema.dump(user)
            print(userFecthed)
            if not errors:
                print("inside"+str(userFecthed))
                return userFecthed
            else:
                raise UserServiceException(errors=errors)
        else:
            print("User not found")
            raise UserNotFoundException


    @rpc
    def getUserById(self, id):
        #self.db.list_collection_names()
        print(id)

        user = User.objects(id=id).first()
        #print(type(user))
        if user is not None:
            userSchema = UserSchema()
            userFecthed,errors = userSchema.dump(user)
            print(userFecthed)
            if not errors:
                print("inside"+str(userFecthed))
                return userFecthed
            else:
                raise UserServiceException(errors=errors)
        else:
            print("User not found")
            raise UserNotFoundException


    @rpc
    def getUserByEmailAndPassword(self, email,password):
        #self.db.list_collection_names()
        print(email)

        user = User.objects(email=email).first()
        #print(type(user))
        #print(user.password)
        if user is not None and check_password_hash(user.password, password):
            userSchema = UserSchema()
            userFecthed,errors = userSchema.dump(user)
            print(userFecthed)
            if not errors:
                print("inside"+str(userFecthed))
                return userFecthed
            else:
                raise UserServiceException(errors=errors)
        else:
            print("User not found")
            raise UserNotFoundException

    @rpc
    def createUser(self,user):
        user['password'] = generate_password_hash(user['password'], method='sha256')
        createdUser = User(**user)
        createdUser.save()
