import asyncio
from logging import Logger, getLogger

from passlib.context import CryptContext


class AsyncArgon2:
    def __init__(self, logger: Logger | None = None, **kwargs) -> None:
        default_params = {
            "time_cost": 2,
            "memory_cost": 102400,
            "parallelism": 8,
            "hash_len": 32,
            "salt_len": 16,
        }
        default_params.update(kwargs)

        self._context = CryptContext(
            schemes=["argon2"], _autoload=True, **default_params
        )
        self.logger = logger or getLogger(__name__)

    async def hash(self, password: str) -> str:
        return await asyncio.to_thread(self._context.hash, password)

    async def verify(self, plain_password: str, password_hash: str) -> bool:
        try:
            return await asyncio.to_thread(
                self._context.verify, plain_password, password_hash
            )
        except Exception as exc:
            self.logger.error("Verification error: %s", str(exc), exc_info=True)
            return False
