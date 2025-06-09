from typing import Annotated
from uuid import uuid4

from sqlalchemy import UUID, String
from sqlalchemy.orm import mapped_column, Mapped

from src.database.db import Base


uuid_pk = Annotated[
    uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4),
]

mapped_str_50_nn = Annotated[
    str, mapped_column(String(50), nullable=False)
]


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid_pk]
    first_name: Mapped[mapped_str_50_nn]
    last_name: Mapped[mapped_str_50_nn]
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
