from typing import List

from pydantic import BaseModel


class Login(BaseModel):
    name: str
    username: str


class LoginGeneratorOutput(BaseModel):
    data: List[Login] = []


class NormalizationOutput(BaseModel):
    original: str
    normalized: str
