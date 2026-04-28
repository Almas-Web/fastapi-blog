from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional,List
from db.models.user import User 
from fastapi import HTTPException
from utils.password_manager import PasswordManager


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    #Get all user with order 
    def get_all_users(self)->List[User]:
        return(
            self.db.query(User)
            .order_by(User.id.desc())
            .all()
        )

    def create_user(
        self,
        email: str,
        password: str,
        is_active: bool = True,
        is_superuser: bool = False
    ) -> User:

        _hashed_password = PasswordManager.get_password_hash(password=password)

        db_user = User(
            email=email,
            password=_hashed_password,
            is_active=is_active,
            is_superuser=is_superuser
        )

        self.db.add(db_user)

        try:
            self.db.commit()
            self.db.refresh(db_user)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        return db_user