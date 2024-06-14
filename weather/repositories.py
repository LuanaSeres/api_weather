from django.conf import settings
import pymongo
from .exceptions import WeatherException
from bson import ObjectId

class WeatherRepository:
    collection = 'weathers'

    def __init__(self, collectionName) -> None:
        self.collection = collectionName

    def getConnection(self):
        client = pymongo.MongoClient(getattr(settings, "MONGO_CONNECTION_STRING"))
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
    
    def get(self, filter):
        documents = []
        for document in self.getCollection().find(filter):
            id = document.pop('_id')
            document['id'] = str(id)
            documents.append(document)
        return documents

    def getByID(self, id):
        document = self.getCollection().find_one({"_id": ObjectId(id)})
        if document:
            id = document.pop('_id')
            document['id'] = str(id)
            return document
        else:
            raise WeatherException("Weather not found")

    def getAll(self):
        documents = []
        for document in self.getCollection().find({}):
            id = document.pop('_id')
            document['id'] = str(id)
            documents.append(document)
        return documents
    
    def getByAttribute(self, attribute, value):
        documents = self.getCollection().find({attribute: value})
        return documents
    
    def insert(self, document):
        self.getCollection().insert_one(document)

    def delete(self, id):
        filter = {"_id": ObjectId(id)}
        self.getCollection().delete_one(filter)

    def update(self, document, id):
        self.getCollection().update_one({"_id": ObjectId(id)}, {"$set": document})

    def deleteAll(self):
        self.getCollection().delete_many({})

    def deleteByID(self, id):
        ret = self.getCollection().delete_one({"_id": ObjectId(id)})
        return ret.deleted_count