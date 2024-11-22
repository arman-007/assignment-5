from pydantic import BaseModel, EmailStr, constr, validator

class UserRegistrationModel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    password: constr(min_length=6)
    role: constr(strip_whitespace=True)

    @validator('role')
    def validate_role(cls, value):
        if value not in ['Admin', 'User']:
            raise ValueError('Role must be either "Admin" or "User"')
        return value

class UserLoginModel(BaseModel):
    email: EmailStr
    password: constr(min_length=6)