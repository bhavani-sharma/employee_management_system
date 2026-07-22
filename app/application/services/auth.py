from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv
from common.data.database import get_db
import infrastructure.schemas.user_schema as userSchema




load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

security = HTTPBearer()

def hash_password(password:str)->str:
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")

def verify_password(password:str, hashed_pw:str)->str:
    return bcrypt.checkpw(password.encode("utf-8")[:72], hashed_pw.encode("utf-8"))

def create_access_token(data:dict, expires_delta: Optional[timedelta]=None)->str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+(expires_delta or timedelta(minutes= ACCESS_TOKEN_EXPIRES_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
) -> userSchema.Users:
    credentials_exc = HTTPException(
        status_code=401,
        detail="unauthorized, could not validate data",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials if credentials else None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = db.query(userSchema.Users).filter(userSchema.Users.email == username).first()
    if user is None:
        raise credentials_exc
    return user
    