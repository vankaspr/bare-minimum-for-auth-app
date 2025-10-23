from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    

class UserLogin(BaseModel):
    login: str # email or username
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool
    
    model_config = ConfigDict(from_attributes=True,)
    
    
class UserAdminResponse(UserResponse):
    pass