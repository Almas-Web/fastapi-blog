from datetime import datetime, timedelta
import os
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.models.user import User
from db.session import get_db
from repositories.user import UserRepository
from schemas.user import Token, UserCreate, UserView
from utils.const import UPLOAD_FOLDER
from utils.jwt_manager import create_access_token, create_refresh_token, verify_token
from utils.password_manager import PasswordManager


router = APIRouter()


# -------------------------
# REGISTER USER
# -------------------------
@router.post("", response_model=UserView)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    user_repo = UserRepository(db=db)

    existing_user = user_repo.get_user_by_email(email=payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists!"
        )

    new_user = user_repo.create_user(
        email=payload.email,
        password=PasswordManager.get_password_hash(payload.password)
    )

    return new_user


# -------------------------
# LOGIN (TOKEN)
# -------------------------
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = UserRepository(db=db).get_user_for_token(
        email=form_data.username,
        password=form_data.password
    )

    token_subject = {"sub": str(user.id)}

    access_token = create_access_token(data=token_subject)
    refresh_token = create_refresh_token(data=token_subject)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# -------------------------
# REFRESH TOKEN
# -------------------------
@router.post("/refresh", response_model=Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):

    payload = verify_token(refresh_token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")

    user = UserRepository(db=db).get_user_by_id(id=int(user_id))

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_subject = {"sub": str(user.id)}

    new_access_token = create_access_token(data=token_subject)
    new_refresh_token = create_refresh_token(data=token_subject)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# -------------------------
# UPLOAD PROFILE IMAGE
# -------------------------
@router.put("/upload_image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(UserRepository.get_current_user),
    db: Session = Depends(get_db)
):

    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    file_content = await file.read()

    max_size = 500 * 1024  # 500KB
    if len(file_content) > max_size:
        raise HTTPException(status_code=400, detail="Image size should not exceed 500KB")

    user_repo = UserRepository(db=db)

    # remove old image
    if current_user.image_url:
        user_repo.remove_previous_image(current_user.image_url)

    unique_filename = f"{uuid4()}_{file.filename}"
    new_file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(new_file_path, "wb") as buffer:
        buffer.write(file_content)

    user_repo.save_image_path_to_db(
        user=current_user,
        new_image_path=unique_filename
    )

    return {
        "success": True,
        "path": f"/static/{unique_filename}"
    }


# -------------------------
# FORGOT PASSWORD
# -------------------------
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid4())
    expire_time = datetime.utcnow() + timedelta(minutes=15)

    user.reset_token = token
    user.reset_token_expire = expire_time

    db.commit()

    return {
        "message": "Reset token generated",
        "reset_token": token
    }


# -------------------------
# RESET PASSWORD
# -------------------------
@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.reset_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if not user.reset_token_expire or user.reset_token_expire < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    # FIXED PASSWORD HASHING
    user.password = PasswordManager.get_password_hash(new_password)

    user.reset_token = None
    user.reset_token_expire = None

    db.commit()

    return {
        "success": True,
        "message": "Password reset successful"
    }