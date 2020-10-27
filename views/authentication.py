from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from models import User

router = APIRouter()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "a201a8de0685659bf1d77bab784a33498eb9b120a14eae0479fac179248e0cc3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24*14

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshedToken(BaseModel):
    access_token: str
    token_type: str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/login")

def verifyPassword(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def getUser(username: str):
    return await User.get(username=username)

async def authenticateUser(username: str, password: str):
    user = await getUser(username)
    if not user:
        return False
    if not verifyPassword(password, user.password_hash):
        return False
    return user

def createAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def createRefreshToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    to_encode.update({"token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def getTokenUser(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expire: int = payload.get("exp")
        token_type: str = payload.get("token_type")
        is_expired: bool = expire < datetime.utcnow().timestamp()
        if username is None or is_expired or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = getUser(username=username)
    if user is None:
        raise credentials_exception
    return user

async def getRefreshUser(refresh:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expire: int = payload.get("exp")
        token_type: str = payload.get("token_type")
        is_expired: bool = expire < datetime.utcnow().timestamp()
        if username is None or is_expired or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await getUser(username=username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = createAccessToken(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = createRefreshToken(
        data={"sub": user.username},
        expires_delta=timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=RefreshedToken)
async def refreshToken(refresh: str):
    user = await getRefreshUser(refresh)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = createAccessToken(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }