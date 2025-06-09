from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    _model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)