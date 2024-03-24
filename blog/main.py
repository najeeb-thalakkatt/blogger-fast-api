# main.py

from fastapi import FastAPI
from routers import users, blogs

app = FastAPI()

app.include_router(users.router)
app.include_router(blogs.router)
