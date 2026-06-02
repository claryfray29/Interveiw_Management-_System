import os
import hashlib
import jwt

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, get_db

SECRET_KEY = os.getenv("KEY") or os.getenv("FALLBACK_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_user(db: Session, role: str, email: str):
    if role == "global_admin":
        return db.query(models.GlobalAdmin).filter(models.GlobalAdmin.email == email).first()
    elif role == "company_admin":
        return db.query(models.CompanyAdmin).filter(models.CompanyAdmin.email == email).first()
    elif role == "interviewer":
        return db.query(models.Interviewer).filter(models.Interviewer.email == email).first()
    elif role == "candidate":
        return db.query(models.Candidate).filter(models.Candidate.email == email).first()
    return None

def authenticate_user(db: Session, role: str, email: str, password: str):
    user = get_user(db, role, email)
    if not user or not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.JWTError:
        raise Exception("Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, role=token_data.role, email=token_data.email)
    if user is None:
        raise credentials_exception

    user.system_role = token_data.role
    return user

async def login_for_access_token(data: schemas.Login, db: Session = Depends(get_db)):
    #role = form_data.scopes[0] if form_data.scopes else "candidate"
    user = authenticate_user(db, data.role, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": data.email, "role": data.role}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}