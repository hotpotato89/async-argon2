import asyncio

from async_argon2 import AsyncArgon2


class TestAsyncArgon2:
    async def test_hash_and_verify(self):
        hasher = AsyncArgon2()
        hashed = await hasher.hash("password123")
        assert hashed is not None
        assert isinstance(hashed, str)
        assert await hasher.verify("password123", hashed) is True

    async def test_verify_wrong_password(self):
        hasher = AsyncArgon2()
        hashed = await hasher.hash("password123")
        assert await hasher.verify("wrong_password", hashed) is False

    async def test_verify_invalid_hash(self):
        hasher = AsyncArgon2()
        result = await hasher.verify("password123", "invalid_hash")
        assert result is False

    async def test_custom_params(self):
        hasher = AsyncArgon2(
            argon2__time_cost=3,
            argon2__memory_cost=153600,
            argon2__parallelism=4,
        )
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_hash_empty_string(self):
        hasher = AsyncArgon2()
        hashed = await hasher.hash("")
        assert hashed is not None
        assert await hasher.verify("", hashed) is True

    async def test_hash_long_password(self):
        hasher = AsyncArgon2()
        long_password = "x" * 1000
        hashed = await hasher.hash(long_password)
        assert await hasher.verify(long_password, hashed) is True

    async def test_concurrent_hashing(self):
        hasher = AsyncArgon2()
        passwords = ["pass1", "pass2", "pass3", "pass4", "pass5"]

        tasks = [hasher.hash(pwd) for pwd in passwords]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(passwords)
        for i, hashed in enumerate(results):
            assert await hasher.verify(passwords[i], hashed) is True

    async def test_verify_concurrent(self):
        hasher = AsyncArgon2()
        password = "test_password"
        hashed = await hasher.hash(password)

        tasks = [hasher.verify(password, hashed) for _ in range(10)]
        results = await asyncio.gather(*tasks)

        assert all(results) is True

    async def test_logger(self):
        import logging

        logger = logging.getLogger("test_logger")
        hasher = AsyncArgon2(logger=logger)
        assert hasher.logger is logger
