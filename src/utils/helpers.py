import jwt
import uuid
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.settings import settings

security = HTTPBearer()
async def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> uuid.UUID:
    try:
        token = credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) 
        user_id_str = payload.get("user_id")
        if not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing user_id")
        return uuid.UUID(str(user_id_str))
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )