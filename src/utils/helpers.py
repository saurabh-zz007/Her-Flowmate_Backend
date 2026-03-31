import jwt
import uuid
def get_user_id(token: str, secret_key:str, algorithm: str):
    try:
        
        payload = jwt.decode(token, secret_key, algorithms=[algorithm]) # type: ignore
        jwt_token = uuid.UUID(payload.get("user_id"))
        return jwt_token
    except jwt.PyJWTError: # type: ignore
        return None