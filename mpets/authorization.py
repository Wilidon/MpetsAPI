import asyncio
import random
import string

from aiohttp import ClientTimeout, ClientSession

from mpets.profile import profile
from mpets.settings import change_pw

from mpets.utils.constants import MPETS_URL


async def start(name, password, type, timeout, connector):
    try:
        if name == "standard":
            session = ClientSession(timeout=timeout, connector=connector)
            await session.get(f"{MPETS_URL}/start")
            resp = await session.get(f"{MPETS_URL}/save_gender?type={type}")
            if "Магазин" in await resp.text():
                cookies = session.cookie_jar.filter_cookies(MPETS_URL)
                for key, cookie in cookies.items():
                    if cookie.key == "PHPSESSID":
                        cookies = {"PHPSESSID": cookie.value}
                    if cookie.key == "id":
                        pet_id = int(cookie.value)
                if password:
                    resp = await change_pw(password, cookies, timeout, connector)
                else:
                    password = (''.join(random.sample(string.ascii_lowercase, k=10)))
                    resp = await change_pw(password, cookies, timeout, connector)
                if resp["status"] is False:
                    return resp
                resp = await profile(pet_id, cookies, timeout, connector)
                if resp["status"] is False:
                    return resp
                return {"status": True,
                        "pet_id": pet_id,
                        "name": resp["name"],
                        "password": password,
                        "cookies": cookies}
            elif "" in await resp.text():
                pass
        else:
            pass
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def login(name, password, timeout, connector):
    try:
        session =  ClientSession(timeout=timeout, connector=connector)
        data = {"name": name, "password": password}
        async with session.post(f"{MPETS_URL}/login",
                                data=data) as resp:
            if "Неправильное Имя или Пароль" in await resp.text():
                return {"status": False,
                        "code": 6,
                        "msg": "Incorrect name or password"}
            elif "Ваш питомец заблокирован" in await resp.text():
                return {"status": False,
                        "code": 7,
                        "msg": "This account has blocked"}
            elif "Магазин" in await resp.text():
                cookies = session.cookie_jar.filter_cookies(MPETS_URL)
                for key, cookie in cookies.items():
                    if cookie.key == "PHPSESSID":
                        cookies = {"PHPSESSID": cookie.value}
                    if cookie.key == "id":
                        pet_id = int(cookie.value)
                return {"status": True,
                        "pet_id": pet_id,
                        "name": name,
                        "cookies": cookies}
    except asyncio.TimeoutError as e:
        return await login(name, password, timeout, connector)
    except Exception as e:
        return {"status": "error",
                "code": 0,
                "msg": e}