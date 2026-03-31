import jwt

def get_user_id(token: str, secret_key:str, algorithm: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm]) # type: ignore
        return payload.get("user_id")
    except jwt.PyJWTError: # type: ignore
        return None