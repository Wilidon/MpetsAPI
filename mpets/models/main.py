from pydantic import BaseModel, Field


class ReturnTrueStatus(BaseModel):
    status: bool


class Profile(BaseModel):
    status: bool
    pet_id: int
    name: str
    password: str
    cookies: dict


class Login(BaseModel):
    """
    This is the description of the main model
    """

    status: bool = Field(...)
    pet_id: int = Field(...)
    name: str = Field(...)
    cookies: dict = Field(...)