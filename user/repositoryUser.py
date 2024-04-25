import pymongo
from bson import ObjectId
from django.conf import settings
from weather.exceptions import WeatherException

class UserRepository:
    collection = ''

    def _init_(self, collectionName) -> None:
        self.collection = collectionName

    def get(self, filter):
        documents = []
        for document in self.getCollection().find(filter):
            id = document.pop('_id')
            document['id'] = str(id)
            documents.append(document)
        return documents

    def getConnection(self):
        try:
            client = pymongo.MongoClient(getattr(settings, "MONGO_CONNECTION_STRING"))
        except:
            raise WeatherException("Error connecting to database")

        connection = client[getattr(settings, "MONGO_DATABASE_NAME")]
        return connection

    def getCollection(self):
        conn = self.getConnection()
        collection = conn[self.collection]
        return collection

    def getByID(self, id):
        document = self.getCollection().find_one({"_id": ObjectId(id)})
        if document:
            id = document.pop('_id')
            document['id'] = str(id)
            return document
        else:
            raise WeatherException("User not found")

    def getAll(self):
        documents = []
        for document in self.getCollection().find({}):
            id = document.pop('_id')
            document['id'] = str(id)
            documents.append(document)
        return documents

    def insert(self, user):
        user_data = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
        }
        self.getCollection().insert_one(user_data)

    def delete(self, id):
        filter = {"_id": ObjectId(id)}
        self.getCollection().delete_one(filter)

    def update(self, user_data, id):
        self.getCollection().update_one({"_id": ObjectId(id)}, {"$set": user_data})

    def deleteByID(self, id):
        ret = self.getCollection().delete_one({"_id": ObjectId(id)})
        return ret.deleted_count