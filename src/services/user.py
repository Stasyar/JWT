from fastapi import HTTPException
from pydantic import UUID4

from src.auth.password import hash_password, verify_password
from src.logger import logger
from src.models.user import User
from src.schemas.user import UserRegisterSchema, UserLoginSchema
from src.services.base_service import BaseService, transaction_mode


class UserService(BaseService):
    _repo = "user"

    @transaction_mode
    async def add_one_and_get_obj(self, user_data: UserRegisterSchema) -> User:
        logger.info("Creating user")

        exists = await self._get_related_repo().get_by_email(user_data.email)

        if not exists:
            data_dict = user_data.model_dump()
            data_dict["password"] = hash_password(user_data.password)
            return await self._get_related_repo().add_one_and_get_obj(data_dict)

        else:
            raise HTTPException(status_code=400, detail="Email already registered")

    @transaction_mode
    async def authenticate(self, user_data: UserLoginSchema) -> User:
        instance = await self._get_related_repo().get_by_email(user_data.email)

        if verify_password(user_data.password, instance.password):
            return instance
        else:
            raise HTTPException(status_code=400, detail="Wrong credentials")
