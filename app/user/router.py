from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from app import db
from app.auth import jwt
from app.user import shema, services, validator

router = APIRouter(tags=["Users"], prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_registration(
    request: shema.User,
    database: Session = Depends(db.get_db)
):
    user_by_email = await validator.verify_email_exist(email=request.email, db=database)
    if user_by_email:
        raise HTTPException(status_code=400, detail="This user with this email already exist in the system")

    user_by_phone = await validator.verify_phone_exist(phone=request.phone, db=database)
    if user_by_phone:
        raise HTTPException(status_code=400, detail="This user with this phone number already exist in the system")

    new_user = await services.new_user_register(request=request, database=database)

    return new_user


@router.get("/", response_model=List[shema.DisplayUser])
async def get_all_users(
    database: Session = Depends(db.get_db),
    current_user: shema.User = Depends(jwt.get_current_user),
):
    return await services.all_users(database=database)


@router.get("/{user_id}", response_model=shema.DisplayUser)
async def get_user_by_id(
    user_id: int,
    database: Session = Depends(db.get_db),
    current_user: shema.User = Depends(jwt.get_current_user),
):
    return await services.get_user_by_id(user_id=user_id, database=database)


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_user_by_id(
    user_id: int,
    database: Session = Depends(db.get_db),
    current_user: shema.User = Depends(jwt.get_current_user),
):
    return await services.delete_user_by_id(user_id=user_id, database=database)
