from typing import Optional
from pydantic import BaseModel


class BlogPostBase(BaseModel):
    title: str
    content: str


class BlogPostCreate(BlogPostBase):
    id: int


class BlogPost(BlogPostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    location: str


class UserCreateResp(BaseModel):
    name: str
    email: str
    id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    blog_posts: list[BlogPost] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
