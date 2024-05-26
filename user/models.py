
class UserEntity:

    def __init__(self, username, id = None, email = None, password = None) -> None:
        self.id = id
        self.email = email
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f'{self.username}: {self.password}'