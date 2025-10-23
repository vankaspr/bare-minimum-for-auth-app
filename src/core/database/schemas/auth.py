from pydantic import BaseModel, EmailStr

class VerifyEmail(BaseModel):
    token: str
    

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    

class ResetPasswordRequest(BaseModel):
    token: str
    password: str