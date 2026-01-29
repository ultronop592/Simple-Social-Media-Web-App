from pydantic import BaseModel
from fastapi_users import schemas
import uuid


class PostCreate(BaseModel):
    title: str
    content: str
    
class PostResponse(BaseModel):
    title: str
    content: str

class userUpdate(BaseModel):
    pass

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass