from datetime import timedelta, datetime, UTC

import jwt

from src.auth.utils import Settings


def encode_jwt(
    payload: dict,
    private_key: str = Settings.private_key_path.read_text(),
    algorithm: str = Settings.algorithm,
    expire_minutes: int = Settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = Settings.public_key_path.read_text(),
    algorithm: str = Settings.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded