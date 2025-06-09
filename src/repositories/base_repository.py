from abc import ABC, abstractmethod
from typing import Any, Generic, Never, TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import delete as sqla_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_404_NOT_FOUND


class AbstractRepository(ABC):
    """An abstract class implementing the CRUD operations for working with any database."""

    @abstractmethod
    async def get_by_email(self, *args: Any, **kwargs: Any) -> Never:
        """Getting an entry by email."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry and getting that entry."""
        raise NotImplementedError


ModelType = TypeVar("ModelType")


class BaseRepository(AbstractRepository, Generic[ModelType]):
    _model: ModelType

    def __init__(self, _session: AsyncSession) -> None:
        self._session = _session

    async def get_by_email(self, email: str) -> ModelType | None:
        stmt = select(self._model).where(self._model.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_one_and_get_obj(self, obj_in: dict) -> ModelType:
        obj = self._model(**obj_in)
        self._session.add(obj)
        return obj




