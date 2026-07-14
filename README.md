## AsyncArgon2

Просто собственная библиотека чтобы запускать хэширование в отдельных потоках и не блокировать `event loop`

### Использование
```python
import asyncio

from async_argon2 import AsyncArgon2

hash_manager = AsyncArgon2()

async def main() -> None:
    password_hash = await hash_manager.hash("secret-password")
    print(password_hash) # Хэш пароля

    assert await hash_manager.verify("secret_password", password_hash)

if __name__ == "__main__":
    asyncio.run(main())

```
