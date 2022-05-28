from dataclasses import dataclass
import hashlib
import uuid
import services.exceptions as errors


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
        encoded = password.encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def check_password(self, password: str) -> bool:
        encoded = password.encode("utf-8")
        password_ = hashlib.sha256(encoded).hexdigest()
        return password_ == self.encrypted_password

    def update_name(self, name: str) -> None:
        self.name = name

    def login(self, password: str) -> bool:
        if self.check_password(password):
            return True
        raise errors.LoginFailure
