from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")

   