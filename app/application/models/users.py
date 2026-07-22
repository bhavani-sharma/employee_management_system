from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    emp_id: str = Field(pattern=r"I-\d+$")
    password: str


class UserRequest(UserBase):
    email: EmailStr
    emp_id: str = Field(pattern=r"I-\d+$")
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    emp_id: str = Field(pattern=r"I-\d+$")
    email:EmailStr

