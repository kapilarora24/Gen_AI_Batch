from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str = None
    email: str = None
    phonenumber: str = None
