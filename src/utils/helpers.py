import jwt
import uuid
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.settings import settings

security = HTTPBearer()
def get_user_id(credentials:HTTPAuthorizationCredentials = Depends(security)):
    print("Extracting user ID from token")
    try:
        token = credentials.credentials
        print(token)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid token format")
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM) 
        user_id = uuid.UUID(payload.get("user_id"))
        return user_id
    except jwt.PyJWTError: # type: ignore
        raise HTTPException(status_code=401, detail="Invalid token")