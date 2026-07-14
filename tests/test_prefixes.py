import pytest

from async_argon2 import AsyncArgon2


class TestArgon2Params:
    async def test_default_params(self):
        """Проверяем параметры по умолчанию"""
        hasher = AsyncArgon2()
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_custom_params_without_prefix(self):
        """Проверяем кастомные параметры без префикса argon2__"""
        hasher = AsyncArgon2(
            time_cost=3,
            memory_cost=153600,
            parallelism=4,
        )
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_custom_params_with_prefix(self):
        """Проверяем кастомные параметры с префиксом argon2__"""
        hasher = AsyncArgon2(
            argon2__time_cost=3,
            argon2__memory_cost=153600,
            argon2__parallelism=4,
        )
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_mixed_params(self):
        """Проверяем смешанные параметры (с префиксом и без)"""
        hasher = AsyncArgon2(
            time_cost=3,
            argon2__memory_cost=153600,
            parallelism=4,
        )
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_partial_params(self):
        """Проверяем частичные параметры (остальные по умолчанию)"""
        hasher = AsyncArgon2(time_cost=3)
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_hash_len_param(self):
        """Проверяем параметр hash_len"""
        hasher = AsyncArgon2(hash_len=64)
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_salt_len_param(self):
        """Проверяем параметр salt_len"""
        hasher = AsyncArgon2(salt_len=32)
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_all_params_without_prefix(self):
        """Проверяем все параметры без префикса"""
        hasher = AsyncArgon2(
            time_cost=3,
            memory_cost=153600,
            parallelism=4,
            hash_len=64,
            salt_len=32,
        )
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True

    async def test_all_params_with_prefix(self):
        """Проверяем все параметры с префиксом"""
        hasher = AsyncArgon2(
            argon2__time_cost=3,
            argon2__memory_cost=153600,
            argon2__parallelism=4,
            argon2__hash_len=64,
            argon2__salt_len=32,
        )
        hashed = await hasher.hash("password123")
        assert await hasher.verify("password123", hashed) is True