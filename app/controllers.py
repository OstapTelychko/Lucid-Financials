from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import HTTPException, status
import sys

from app.schemas import UserWithToken
from app.models import User, Post
from app.auth import get_password_hash, create_access_token, authenticate_user
from app.cache import get_cached_posts, set_cached_posts
from project.settings import MAX_POST_SIZE

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.schemas import UserLogin, PostCreate


def create_user(db: Session, user: UserLogin):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.email})
    return UserWithToken(access_token=access_token, user=db_user)


def login(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}


def create_post(db: Session, post: PostCreate, user: User):
    # Check payload size
    payload_size = sys.getsizeof(post.text)
    if payload_size > MAX_POST_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Post size exceeds maximum allowed size of {MAX_POST_SIZE} bytes"
        )
    
    # Also store in database (keeping original functionality)
    db_post = Post(**post.model_dump(), owner_id=user.id)
    db.add(db_post)
    db.commit()


def get_posts(db: Session, user: User):
    cached_posts = get_cached_posts(user.id)
    if cached_posts:
        return cached_posts
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    set_cached_posts(user.id, posts)
    return posts


def delete_post(db: Session, post_id: int, user: User):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}
