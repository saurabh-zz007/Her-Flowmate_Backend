from pydantic import BaseModel

class authData(BaseModel):
    token: str