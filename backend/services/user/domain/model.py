from dataclasses import dataclass
import hashlib
import uuid
import backend.services.exceptions as errors


@dataclass
class User:
    name: str
    email: str
    password: str
    deleted: bool = False
    encrypted_password: str = None
    id: str = str(uuid.uuid4())

    def __post_init__(self):
        if not self.encrypted_password:
            self.encrypted_password = self.encrypt_password(self.password)
        # removing plaintext password from object
        self.password = ""

    def encrypt_password(self, password: str) -> str:
        """Encrypt the password with one way hash sha256 algorithm"""
        encoded = password.encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def check_password(self, password: str) -> bool:
        """Creates sha256 hash for the given password and check if the stored hash in object is same or not"""
        encoded = password.encode("utf-8")
        password_ = hashlib.sha256(encoded).hexdigest()
        return password_ == self.encrypted_password

    def update_name(self, name: str) -> None:
        self.name = name
