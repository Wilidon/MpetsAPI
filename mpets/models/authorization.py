from pydantic import BaseModel


class Start(BaseModel):
    status: bool
    pet_id: int
    name: str
    password: str
    cookies: dict


class Login(BaseModel):
    status: bool
    pet_id: int
    name: str
    cookies: dict