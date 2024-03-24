# routers/blogs.py

from routers import users
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
import auth
import schemas
import service
from database import SessionLocal, engine

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/users/blog_posts/", response_model=schemas.BlogPost)
def create_blog_post_for_user(
        blog_post: schemas.BlogPostCreate,
        current_user: int = Depends(auth.get_current_user)):
    return service.create_user_blog_post(blog_post=blog_post, user_id=current_user)


@router.get("/users/{user_id}/blog_posts/", response_model=List[schemas.BlogPostCreate])
def read_blog_posts_for_user(
        user_id: int,
        current_user: int = Depends(auth.get_current_user)):
    blog_posts = service.get_blog_posts_by_user(user_id=user_id)
    return blog_posts
