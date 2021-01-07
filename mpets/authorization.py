import random
import string

from aiohttp import ClientTimeout, ClientSession

from mpets.profile import profile
from mpets.settings import change_pw


async def start(name, password, type, timeout, connector):
    try:
        if name == "standard":
            async with ClientSession(timeout=timeout, connector=connector) as session:
                await session.get("https://mpets.mobi/start")
                resp = await session.get(f"https://mpets.mobi/save_gender?type={type}")
                if "Магазин" in await resp.text():
                    cookies = session.cookie_jar.filter_cookies("https://mpets.mobi")
                    for key, cookie in cookies.items():
                        if cookie.key == "PHPSESSID":
                            cookies = {'PHPSESSID': cookie.value}
                        if cookie.key == "id":
                            pet_id = cookie.value
                    if password:
                        resp = await change_pw(password, cookies, timeout, connector)
                    else:
                        password = (''.join(random.sample(string.ascii_lowercase, k=10)))
                        resp = await change_pw(password, cookies, timeout, connector)
                    if resp["status"] == "error":
                        return resp
                    resp = await profile(pet_id, cookies, timeout, connector)
                    if resp["status"] == "error":
                        return resp
                    return {"status": "ok",
                            "pet_id": pet_id,
                            "name": resp['name'],
                            "password": password,
                            "cookies": cookies}
                elif "" in await resp.text():
                    pass
                elif "" in await resp.text():
                    pass
            
    except Exception as e:
        return {"status": "error",
                "code": 1,
                "msg": e}


async def login(name, password, connector):
    try:
        async with ClientSession(timeout=ClientTimeout(total=10), connector=connector) as session:
            async with session.post('http://mpets.mobi/login',
                                    data={'name': name, 'password': password}) as resp:
                if "Неправильное Имя или Пароль" in await resp.text():
                    return {"status": "error",
                            "code": 0,
                            "msg": "Incorrect name or password"}
                elif "Ваш питомец заблокирован" in await resp.text():
                    return {"status": "error",
                            "code": 0,
                            "msg": "This account has blocked"}
                elif "Магазин" in await resp.text():
                    cookies = session.cookie_jar.filter_cookies('http://mpets.mobi')
                    for key, cookie in cookies.items():
                        if cookie.key == "PHPSESSID":
                            cookies = {'PHPSESSID': cookie.value}
                        if cookie.key == "id":
                            pet_id = cookie.value
                    return {"status": "ok",
                            "pet_id": pet_id,
                            "cookies": cookies}
    except:
        return {'status': 'error',
                'code': 3,
                'msg': 'Authorization failed'}