from pydantic import BaseModel


class LoginCredentialsModel(BaseModel):
    username: str
    password: str


class LoginModel(BaseModel):
    user: LoginCredentialsModel


class SignUpCredentialsModel(BaseModel):
    username: str
    email: str
    password: str


class SignUpModel(BaseModel):
    user: SignUpCredentialsModel