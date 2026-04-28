from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from db.models.blog import Blog
from schemas.blog import BlogCreate, BlogPagination, BlogUpdate
from slugify import slugify


class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    # ================= HELPER =================
    def get_blog_or_404(self, blog_id: int) -> Blog:
        db_blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
        if not db_blog:
            raise HTTPException(
                status_code=404,
                detail="Blog not found"
            )
        return db_blog

    # ================= CREATE BLOG =================
    def create_blog(self, blog: BlogCreate, author_id: int) -> Blog:
        db_blog = Blog(
            title=blog.title,
            slug=blog.slug,
            content=blog.content,
            is_active=blog.is_active,
            author_id=author_id
        )
        try:
            self.db.add(db_blog)
            self.db.commit()
            self.db.refresh(db_blog)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Something went wrong!"
            )

        return db_blog

    # ================= GET ALL BLOGS =================
    def get_blogs(self, skip: int = 0, limit: int = 100) -> BlogPagination:
        total_count = self.db.query(func.count(Blog.id)).scalar()
        blogs = self.db.query(Blog).offset(skip).limit(limit).all()

        return BlogPagination(
            total_count=total_count,
            skip=skip,
            limit=limit,
            data=blogs
        )

    # ================= GET SINGLE BLOG =================
    def get_blog(self, blog_id: int) -> Blog:
        return self.get_blog_or_404(blog_id)

    # ================= UPDATE BLOG =================
    def update_blog(self, blog_id: int, blog: BlogUpdate) -> Blog:
        db_blog = self.get_blog_or_404(blog_id)

        if blog.title is not None:
            db_blog.title = blog.title
            db_blog.slug = f"{slugify(blog.title)}-{blog_id}"

        if blog.content is not None:
            db_blog.content = blog.content

        if blog.is_active is not None:
            db_blog.is_active = blog.is_active

        self.db.commit()
        self.db.refresh(db_blog)
        return db_blog

    # ================= DELETE BLOG =================
    def delete_blog(self, blog_id: int) -> bool:
        db_blog = self.get_blog_or_404(blog_id)

        self.db.delete(db_blog)
        self.db.commit()
        return True