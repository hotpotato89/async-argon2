# AsyncArgon2

Асинхронная обёртка для хэширования паролей с Argon2.

## Особенности

- **Не блокирует event loop** — хэширование выполняется в отдельном потоке
- **Простой API** — всего два метода: `hash` и `verify`
- **Гибкая настройка** — все параметры Argon2 доступны
- **Type hints** — полная поддержка типов
- **100% тестов** — покрытие кода тестами

## Быстрый старт

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

## Зачем это нужно?

Синхронный Argon2 блокирует event loop при хэшировании:

```python
from argon2 import PasswordHasher

hasher = PasswordHasher()
hashed = hasher.hash("password")  # ❌ Блокирует event loop
```

`AsyncArgon2` решает эту проблему:

```python
from async_argon2 import AsyncArgon2

hasher = AsyncArgon2()
hashed = await hasher.hash("password")  # ✅ Event loop свободен
```

## Установка

```bash
pip install async-argon2
```