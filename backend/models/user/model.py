from dataclasses import dataclass
import hashlib
import uuid


@dataclass
class User:
    id: str
    name: str
    email: str
    password: str

    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())
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

    def login(self, password):
        if self.check_password(password):
            return True
        return False
