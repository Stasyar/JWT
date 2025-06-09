from pydantic import BaseModel, UUID4, Field, model_validator, field_validator, EmailStr


class UserResponseSchema(BaseModel):
    result: bool
    user_id: UUID4



class UserRegisterSchema(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    repeat_password: str = Field(exclude=True)

    @field_validator('first_name', 'last_name')
    @classmethod
    def name_must_be_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('Name must contain only letters')
        return v

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.repeat_password:
            raise ValueError('Passwords do not match')
        return self


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"