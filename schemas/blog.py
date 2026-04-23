from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List   # ✅ FIX
from slugify import slugify
import time
from schemas.user import UserView


class BlogCreate(BaseModel):
    title: str
    content: str
    is_active: bool = False
    slug: Optional[str] = None

    @classmethod
    def create_slug(cls, title: str) -> str:
        _slugify = slugify(title)
        _time_hash = hash(time.time())
        return f"{_slugify}-{_time_hash}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.title:
            self.slug = self.create_slug(self.title)


class BlogSingleRead(BaseModel):
    id: int
    content: str
    slug: str
    created_at: datetime
    author: UserView

    class Config:
        orm_mode = True


class BlogPagination(BaseModel):
    total_count: int
    skip: int
    limit: int
    data: List[BlogSingleRead]

    class Config:
        orm_mode = True

class BlogUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_active: bool = False
    slug: Optional[str] = None

    @classmethod
    def create_slug(cls, title: str) -> str:
        _slugify = slugify(title)
        _time_hash = hash(time.time())
        return f"{_slugify}-{_time_hash}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.title:
            self.slug = self.create_slug(self.title)
