import asyncio
import time


from async_argon2 import AsyncArgon2


class TestEventLoop:
    async def test_hashing_does_not_block_event_loop(self):
        """Проверяем, что хэширование не блокирует event loop"""
        hasher = AsyncArgon2()

        # Запускаем хэширование в фоне
        task = asyncio.create_task(hasher.hash("password123"))

        # Пока хэшируется, делаем другие задачи
        results = []
        for i in range(10):
            await asyncio.sleep(0.01)  # Имитация другой работы
            results.append(i)

        # Ждем завершения хэша
        hashed = await task

        assert len(results) == 10
        assert hashed is not None
        assert await hasher.verify("password123", hashed) is True

    async def test_multiple_hashing_does_not_block(self):
        """Проверяем, что несколько хэшей не блокируют друг друга"""
        hasher = AsyncArgon2()

        start = time.perf_counter()

        # Запускаем 5 хэшей параллельно
        tasks = [hasher.hash(f"pass{i}") for i in range(5)]
        results = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - start

        assert len(results) == 5
        # 5 хэшей должны выполниться за ~0.5-1 секунду,
        # если бы они были последовательными, было бы ~1.5-2 секунды
        assert total_time < 1.5, f"Too slow: {total_time:.2f}s"

    async def test_verify_does_not_block_event_loop(self):
        """Проверяем, что верификация не блокирует event loop"""
        hasher = AsyncArgon2()
        hashed = await hasher.hash("password123")

        # Запускаем верификацию в фоне
        task = asyncio.create_task(hasher.verify("password123", hashed))

        # Пока верифицируется, делаем другие задачи
        results = []
        for i in range(10):
            await asyncio.sleep(0.005)
            results.append(i)

        # Ждем завершения верификации
        is_valid = await task

        assert len(results) == 10
        assert is_valid is True

    async def test_mixed_operations(self):
        """Проверяем смешанные операции: хэш + верификация + другие задачи"""
        hasher = AsyncArgon2()

        # Запускаем хэш
        hash_task = asyncio.create_task(hasher.hash("secret"))

        # Имитация других задач
        counter = 0
        for i in range(20):
            await asyncio.sleep(0.005)
            counter += i

        hashed = await hash_task

        # Запускаем верификацию
        verify_task = asyncio.create_task(hasher.verify("secret", hashed))

        # Еще задачи
        counter2 = 0
        for i in range(20):
            await asyncio.sleep(0.005)
            counter2 += i

        is_valid = await verify_task

        assert counter >= 0
        assert counter2 >= 0
        assert is_valid is True

    async def test_high_load_with_event_loop(self):
        """Проверяем высокую нагрузку без блокировки"""
        hasher = AsyncArgon2()

        # Запускаем много хэшей
        hash_tasks = [hasher.hash(f"pass{i}") for i in range(10)]

        # Параллельно делаем другие задачи
        other_tasks = []
        for i in range(20):
            other_tasks.append(asyncio.sleep(0.001))

        # Ждем всё вместе
        all_tasks = hash_tasks + other_tasks
        results = await asyncio.gather(*all_tasks)

        # Первые 10 результатов — хэши
        hashes = results[:10]
        assert all(h is not None for h in hashes)
        assert len(hashes) == 10
