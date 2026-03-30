from pydantic import BaseModel
from typing import Literal
class UserSchema(BaseModel):
    id: str
    email: str
    display_name: str
    photo_url: str
    age: int
    goal: str = 'track_cycle'
    is_minimal_mode: bool = False

class UserUpdateSchema(BaseModel):
    email: str|None = None
    display_name: str|None = None
    photo_url: str|None = None
    age: int|None = None
    goal: str|None = None
    is_minimal_mode: bool|None = None
