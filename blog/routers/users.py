# routers/users.py

import service
import schemas
import auth
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import datetime

router = APIRouter()


@router.post("/users/", response_model=schemas.UserCreateResp)
def create_user(user: schemas.UserCreate):
    db_user = service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(user=user)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.get_user_by_email(email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(
        minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(
    current_user: int = Depends(auth.get_current_user)
):
    return {"user_id": current_user}


@router.put("/users/me", response_model=schemas.UserUpdate)
def update_user(
        user_update: schemas.UserUpdate,
        current_user: int = Depends(auth.get_current_user)):
    db_user = service.update_user(
        user_id=current_user, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
