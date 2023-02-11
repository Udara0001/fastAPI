from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class userout(BaseModel):
    id :int
    email: EmailStr

    class Config:
        orm_mode = True



class PostBase(BaseModel):
    title :str
    content: str
    published : bool=True



class Postcreste(PostBase):
    pass


class Post(PostBase):
    id:int

    created_at:datetime
    owner_id :int
    owner:userout

    class Config:
        orm_mode = True


class Postout(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode = True







class usercreate(BaseModel):
    email:EmailStr
    passwaord:str




class Userlogin(BaseModel):
    email: EmailStr
    passwaord: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class vote(BaseModel):
    post_id:int
    dir:conint(le=1)

