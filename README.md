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
    mpets = MpetsApi(name="nick", password="password", timeout=5, fast_mode=True)
    await mpets.login()
    
    profile = await mpets.profile()
    print(profile)

asyncio.run(main())
```
