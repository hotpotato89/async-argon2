# API Reference

## AsyncArgon2

### `__init__`

```python
def __init__(self, logger: Logger | None = None, **kwargs) -> None
```

**Параметры**:

 - `logger`: Опциональный логгер
 - `**kwargs`: Параметры Argon2 (time_cost, memory_cost, parallelism, hash_len, salt_len)
    - `time_cost` — количество итераций (по умолчанию 2)
    - `memory_cost` — память в KiB (по умолчанию 102400)
    - `parallelism` — количество потоков (по умолчанию 8)
    - `hash_len` — длина хэша в байтах (по умолчанию 32)
    - `salt_len` — длина соли в байтах (по умолчанию 16)

### `hash`

```python
async def hash(self, password: str) -> str
```

Асинхронно хэширует пароль.

**Аргументы**:

 - `password: str` - пароль в открытом виде

**Возвращает**:
 - `str` - хэш пароля

**Пример**:

```python
hasher = AsyncArgon2()
hashed = await hasher.hash("secret")
```

### `verify`

```python
async def verify(self, plain_password: str, password_hash: str) -> bool
```

Асинхронно проверяет пароль на соответствие хэшу.

**Аргументы**:

 - `plain_password: str` - пароль в открытом виде
 - `password_hash: str` - хэш для проверки

**Возвращает**:

 - `bool` - если если пароль соответствует `True`, иначе - `False`

**Пример**:

```python
hasher = AsyncArgon2()
is_valid = await hasher.verify("secret", hashed)
```