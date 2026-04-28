from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from repositories.blog import BlogRepository
from schemas.blog import BlogCreate, BlogPagination, BlogSingleRead, BlogUpdate

router = APIRouter()


@router.post("", response_model=BlogSingleRead)
def create_blog(payload: BlogCreate, db: Session = Depends(get_db)):
    blog_repo = BlogRepository(db=db)
    new_blog = blog_repo.create_blog(blog=payload, author_id=2)
    return new_blog


@router.get("", response_model=BlogPagination)
def get_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blog_repo = BlogRepository(db=db)
    return blog_repo.get_blogs(skip=skip, limit=limit)


# ✅ FIXED SINGLE BLOG ROUTE
@router.get("/{blog_id}", response_model=BlogSingleRead)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_repo = BlogRepository(db=db)
    return blog_repo.get_blog(blog_id=blog_id)

@router.put("/{blog_id}")
def update_blog(
    blog_id: int,
    payload: BlogUpdate,
    db: Session = Depends(get_db)
):
    blog_repo = BlogRepository(db=db)
    updated_blog = blog_repo.update_blog(blog_id=blog_id, blog=payload)

    return {
        "success": True,
        "message": "Blog updated successfully",
        "data": updated_blog
    }

@router.delete("/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db)):
    blog_repo = BlogRepository(db=db)
    blog_repo.delete_blog (blog_id=blog_id)

    return {
        "message": "Blog deleted successfully"
    }