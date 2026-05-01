from passlib.context import CryptContext
import hashlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class PasswordManager():

    @staticmethod
    def verify_password(plain_password, hashed_password):
        hashed_plain = hashlib.sha256(plain_password.encode()).hexdigest()
        return pwd_context.verify(hashed_plain, hashed_password)

    @staticmethod
    def get_password_hash(password):

        hashed = hashlib.sha256(password.encode()).hexdigest()
        return pwd_context.hash(hashed)