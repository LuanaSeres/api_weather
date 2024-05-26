import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import UserEntity
from .repository import UserRepository
import pymongo

def authenticate(username, password):
    client = pymongo.MongoClient('mongodb://10.109.2.63:443/')
    db = client['weather_luana']
    users_collection = db['users']
    
    user_data = users_collection.find_one({'username': username, 'password': password})
    client.close()
    
    if user_data:
        return UserEntity(username=user_data['username'], email=user_data['email'], password=user_data['password']) 
    else:
        return None


def generateToken(user):
    payload = {
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(payload=payload, key=getattr(settings, "SECRET_KEY"), algorithm='HS256')

def refreshToken(user):
    return generateToken(user)

def verifyToken(token):
    error_code = 0
    payload = None
    try:
        payload = jwt.decode(jwt=token, key=getattr(settings, "SECRET_KEY"), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        error_code = 1
    except jwt.InvalidTokenError:
        error_code = 2

    return [error_code, payload]

def getAuthenticatedUser(token):
    _, payload = verifyToken(token)

    if payload is not None:
        repository = UserRepository(collectionName='users')
        user_data = repository.get({'username': payload['username']})
        if user_data:
            return UserEntity(username=user_data[0]['username'], email=user_data[0]['email'], password=user_data[0]['password'])
    return None