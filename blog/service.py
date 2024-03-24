# service.py

import auth
import models
import schemas
from database import SessionLocal

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


db = get_db()

# User CRUD operations


def get_user(user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(email=user.email, name=user.name,
                          location=user.location, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Blog post CRUD operations


def get_blog_posts_by_user(user_id: int):
    return db.query(models.BlogPost).filter(models.BlogPost.owner_id == user_id).all()


def create_user_blog_post(blog_post: schemas.BlogPostCreate, user_id: int):
    db_blog_post = models.BlogPost(**blog_post.dict(), owner_id=user_id)
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post


def update_user(user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.name = user_update.name
    db_user.location = user_update.location
    db.commit()
    db.refresh(db_user)
    return db_user
