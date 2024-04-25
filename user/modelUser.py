from django.db import models

class User:
    def __init__(self, username, email, password, id=None):
        self.username = username
        self.email = email
        self.password = password
        self.id = id

    def __str__(self):
        return f"User <{self.username}>"