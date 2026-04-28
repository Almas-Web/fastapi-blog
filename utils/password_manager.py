from passlib.context import CryptContext
import hashlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class PasswordManager():

    @staticmethod
    def verify_password(plain_password, hashed_password):
        # Step 1: sha256 apply
        hashed_plain = hashlib.sha256(plain_password.encode()).hexdigest()
        
        # Step 2: bcrypt verify
        return pwd_context.verify(hashed_plain, hashed_password)

    @staticmethod
    def get_password_hash(password):
        # Step 1: sha256 apply
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        # Step 2: bcrypt hash
        return pwd_context.hash(hashed)