# Быстрый старт

## Базовое использование

```python
import asyncio
from async_argon2 import AsyncArgon2

hasher = AsyncArgon2()

async def main():
    # Хэширование
    hashed = await hasher.hash("my_secret_password")
    print(f"Хэш: {hashed}")

    # Верификация
    is_valid = await hasher.verify("my_secret_password", hashed)
    print(f"Пароль верный: {is_valid}")  # True

    is_valid = await hasher.verify("wrong_password", hashed)
    print(f"Пароль верный: {is_valid}")  # False

asyncio.run(main())
```

## В `FastAPI`

```python
from fastapi import FastAPI, HTTPException, status
from async_argon2 import AsyncArgon2
from pydantic import BaseModel

app = FastAPI()
hasher = AsyncArgon2()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/register")
async def register(data: RegisterRequest):
    hashed = await hasher.hash(data.password)
    # Сохраняем hashed в БД
    return {"message": "User created"}

@app.post("/login")
async def login(data: LoginRequest):
    # Достаём хэш из БД
    stored_hash = "..."
    is_valid = await hasher.verify(data.password, stored_hash)
    if not is_valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}
```