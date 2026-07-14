import asyncio
from logging import Logger, getLogger

from passlib.context import CryptContext


class AsyncArgon2:
    """
    Асинхронная обёртка для хэширования паролей с Argon2.

    Запускает хэширование в отдельном потоке, не блокируя event loop.
    """

    def __init__(self, logger: Logger | None = None, **kwargs) -> None:
        """
        Инициализация AsyncArgon2.

        Args:
            logger: Опциональный логгер. Если не передан, создаётся автоматически.
            **kwargs: Параметры Argon2:
                - time_cost: Количество итераций (по умолчанию 2)
                - memory_cost: Используемая память в KiB (по умолчанию 102400)
                - parallelism: Количество потоков (по умолчанию 8)
                - hash_len: Длина хэша в байтах (по умолчанию 32)
                - salt_len: Длина соли в байтах (по умолчанию 16)
        """
        default_params = {
            "argon2__time_cost": 2,
            "argon2__memory_cost": 102400,
            "argon2__parallelism": 8,
            "argon2__hash_len": 32,
            "argon2__salt_len": 16,
        }
        default_params.update(kwargs)

        self._context = CryptContext(
            schemes=["argon2"], _autoload=True, **default_params
        )
        self.logger = logger or getLogger(__name__)

    async def hash(self, password: str) -> str:
        """
        Асинхронно хэширует пароль.

        Args:
            password: Пароль в виде строки.

        Returns:
            str: Хэшированный пароль.

        Example:
            >>> hasher = AsyncArgon2()
            >>> hashed = await hasher.hash("secret")
            >>> print(hashed[:20])
            $argon2id$v=19$m=102400...
        """
        return await asyncio.to_thread(self._context.hash, password)

    async def verify(self, plain_password: str, password_hash: str) -> bool:
        """
        Асинхронно проверяет пароль на соответствие хэшу.

        Args:
            plain_password: Пароль в открытом виде.
            password_hash: Хэш для проверки.

        Returns:
            bool: True если пароль соответствует хэшу, иначе False.
        """
        try:
            return await asyncio.to_thread(
                self._context.verify, plain_password, password_hash
            )
        except Exception as exc:
            self.logger.error("Verification error: %s", str(exc), exc_info=True)
            return False