# MpetsAPI

API для игры Удивительные питомцы.

### Установка

1. Иметь ```python3.7+```
2. Скачать и распаковать в папку с проектом.

### Пример использования.
Все доступные методы находятся в файле __init__.py
```python
import asyncio

from mpets import MpetsApi


async def main():
    mpets = MpetsApi(name="name", password="password", timeout=5, fast_mode=True)
    resp = await mpets.login()
    if resp.status is False:
        print(f"Авторизация не прошла: {resp}")
        return False
    profile = await mpets.profile()
    if profile.status is False:
        print(f"Не удалось получить профиль: {resp}")
    print(f"Nick: {profile.name}")

if __name__ == '__main__':
    asyncio.run(main())
```
