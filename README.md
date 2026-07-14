# AsyncArgon2

[![PyPI version](https://img.shields.io/pypi/v/async-argon2.svg)](https://pypi.org/project/async-argon2/)
[![License](https://img.shields.io/github/license/hotpotato89/async-argon2.svg)](https://github.com/hotpotato89/async-argon2/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/hotpotato89/async-argon2/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/hotpotato89/async-argon2)

Асинхронная обертка для хэширования паролей с Argon2.

[**Документация**](https://hotpotato89.github.io/async-argon2/)

## Установка

```bash
pip install async-argon2
```

## Использование

```python
import asyncio
from async_argon2 import AsyncArgon2

hasher = AsyncArgon2()

async def main():
    hashed = await hasher.hash("password123")
    print(hashed)
    
    is_valid = await hasher.verify("password123", hashed)
    print(is_valid)  # True

asyncio.run(main())
```

## Почему AsyncArgon2?

Синхронный Argon2 блокирует event loop. `AsyncArgon2` запускает хэширование в отдельном потоке, не блокируя другие задачи.

```python
# ❌ Блокирует event loop
from argon2 import PasswordHasher
hasher = PasswordHasher()
hashed = hasher.hash("password")  # Все ждут!

# ✅ Не блокирует
from async_argon2 import AsyncArgon2
hasher = AsyncArgon2()
hashed = await hasher.hash("password")  # Event loop свободен
```

## Кастомные параметры

```python
hasher = AsyncArgon2(
    time_cost=3,
    memory_cost=153600,
    parallelism=4,
)
```
