from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False,index=True)
    password=Column(String,nullable=False)
    is_superuser=Column(Boolean(),default=False)
    is_active = Column(Boolean(), default=True)
    blogs = relationship("Blog", back_populates="author")
    image_url=Column(String,nullable=True)

    #  add these 2 fields
    reset_token = Column(String, nullable=True)
    reset_token_expire = Column(DateTime, nullable=True)