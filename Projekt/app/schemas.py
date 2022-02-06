from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True # Default True

class PostCreate(PostBase):
    pass

# User Stuff

class UserCreate(BaseModel):
    email: EmailStr #Selleks vaja emaild-validator lib, mis tuli pip install fastapi[all]-iga koos.
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


## Response

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # Class alt poolt - see skeem, mille mis kehtib ka Get Useri puhul.
    
    class Config: # Selleks, et pydantic oskaks lugeda sqlalchemy type modelit mida talle et antakse
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #int that can be only 0 or 1 (and also negative, but that should be fine)
    
