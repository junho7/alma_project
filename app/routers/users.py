from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import motor.motor_asyncio
from app.utils.auth import create_access_token
from app.models.database import users_collection as collection

from app.utils.auth import get_password_hash

router = APIRouter()

# Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Signup
@router.post("/signup")
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = {}
    user_dict['username'] = form_data.username
    # Check if username already exists
    existing_user = await collection.find_one({"username": user_dict['username']})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already registered")

    # Hash the password
    hashed_password = get_password_hash(form_data.password)
    user_dict["password"] = hashed_password
    # Insert user document
    await collection.insert_one(user_dict)
    return {"message": "User created successfully"}

# token generation
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # If authentication is successful, return a JWT token:
    # Retrieve User from Database
    user = await collection.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Verify Password
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(
        data={
            "sub": form_data.username
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}