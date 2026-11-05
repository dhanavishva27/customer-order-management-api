
import os
import secrets

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas import LoginRequest, TokenResponse


# Load environment variables
load_dotenv()


# Authentication configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

if not all([SECRET_KEY, AUTH_USERNAME, AUTH_PASSWORD]):
    raise RuntimeError("Authentication configuration is missing from .env")


# Create authentication router
router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


# Bearer token security
security = HTTPBearer(auto_error=False)


# Generate JWT token
def create_access_token(username: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# LOGIN API
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):

    username_valid = secrets.compare_digest(
        credentials.username,
        AUTH_USERNAME
    )

    password_valid = secrets.compare_digest(
        credentials.password,
        AUTH_PASSWORD
    )

    if not (username_valid and password_valid):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(credentials.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# VERIFY JWT TOKEN
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication token missing",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username != AUTH_USERNAME:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
