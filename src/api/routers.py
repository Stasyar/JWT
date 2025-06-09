from fastapi import Depends, APIRouter

from src.auth.jwt import encode_jwt
from src.schemas.user import UserResponseSchema, UserRegisterSchema, TokenSchema, UserLoginSchema
from src.services.user import UserService

router = APIRouter(prefix="/auth")


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


@router.post("/register", status_code=201)
async def register(
        user_data: UserRegisterSchema,
        user_service: UserService = Depends(UserService)
) -> UserResponseSchema:

    new_user = await user_service.add_one_and_get_obj(user_data)
    return UserResponseSchema(
        result=True,
        user_id=new_user.id
    )


@router.post("/login", response_model=TokenSchema)
async def login(
        user_data: UserLoginSchema,
        user_service: UserService = Depends(UserService)
) -> TokenSchema:
    user = await user_service.authenticate(user_data)
    token = encode_jwt({"sub": user.email})
    return TokenSchema(access_token=token)


