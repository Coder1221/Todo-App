from dataclasses import dataclass
import hashlib


@dataclass
class User:
    id: str
    name: str
    email: str
    password: str

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = self.encrypt_password(password)

    def encrypt_password(self, password):
        encoded = password.encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def check_password(self, password):
        encoded = password.encode("utf-8")
        password_ = hashlib.sha256(encoded).hexdigest()
        return password_ == self.password

    def update_name(self, name):
        self.name = name
