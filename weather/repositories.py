from django.conf import settings
import pymongo
from .exceptions import WeatherException

class WeatherRepository:
    collection = ''

    def __init__(self, collectionName) -> None:
        self.collection = collectionName

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
    
    def getById(self, id):
        document = self.getCollection().find_one({"_id": id})
        return document
    
    def getAll(self):
        documents = self.getCollection().find({})
        return documents
    
    def getByAttribute(self, attribute, value):
        documents = self.getCollection().find({attribute: value})
        return documents
    
    def insert(self, document):
        self.getCollection().insert_one(document)

    def delete(self, id):
        self.getCollection().delete_one({"_id": id})

    def deleteAll(self):
        self.getCollection().delete_many({})