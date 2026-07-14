# Кастомные параметры

## Все параметры Argon2

```python
hasher = AsyncArgon2(
    argon2__time_cost=3,          # Количество итераций
    argon2__memory_cost=153600,   # Память в KiB (150 MB)
    argon2__parallelism=4,        # Количество потоков
    argon2__hash_len=32,          # Длина хэша в байтах
    argon2__salt_len=16,          # Длина соли в байтах
)
```

## Рекомендации

| Параметр | Значение | Описание |
|----------|----------|----------|
| `time_cost` | 2-3 | Чем выше, тем безопаснее, но медленнее |
| `memory_cost` | 102400-153600 | Память в KiB. 100 MB - хороший баланс |
| `parallelism` | 4-8 | Количество потоков |

## Использование с разными параметрами

```python
# Для регистрации — безопаснее
register_hasher = AsyncArgon2(time_cost=3, memory_cost=153600)

# Для логина — быстрее
login_hasher = AsyncArgon2(time_cost=2, memory_cost=102400)
```