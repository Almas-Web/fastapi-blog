from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from repositories.user import UserRepository
from schemas.user import UserCreate, UserView

router = APIRouter()


@router.post("", response_model=UserView)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db=db)

    existing_user = user_repo.get_user_by_email(email=payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists!"
        )

    new_user = user_repo.create_user(
        email=payload.email,
        password=payload.password
    )

    return new_user   # ✅ cleaner