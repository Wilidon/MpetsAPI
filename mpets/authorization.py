import asyncio
import os
import random
import string
import time

from aiohttp import ClientSession
from python_rucaptcha import ImageCaptcha

from mpets.main import user_agreement
from mpets.profile import profile
from mpets.settings import change_pw

from mpets.utils.constants import MPETS_URL


async def start(name, password, type, timeout, connector):
    try:
        if name == "standard":
            session = ClientSession(timeout=timeout, connector=connector)
            await session.get(f"{MPETS_URL}/start")
            resp = await session.get(f"{MPETS_URL}/save_gender?type={type}")
            await session.close()
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
                await user_agreement(agreement_confirm=True,
                                     params=1,
                                     cookies=cookies,
                                     timeout=timeout,
                                     connector=connector)
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


async def get_captcha(timeout, connector):
    try:
        session = ClientSession(timeout=timeout, connector=connector)
        resp = await session.get('http://mpets.mobi/captcha?r=281')
        await session.close()
        # Снизу говнокод, когда-нибудь, возможно, кем-то он будет исправлен.
        # TODO add pet_id
        for item in resp.cookies.items():
            cookies = str(item[1]).split("=")[1].split(";")[0]
        cookies = {"PHPSESSID": cookies}
        filename = f"{str(time.time())}.jpg"
        with open(filename, 'wb') as fd:
            fd.write(await resp.read())
        return {"status": True,
                "captcha": filename,
                "cookies": cookies}
    except asyncio.TimeoutError as e:
        return await get_captcha(timeout, connector)


async def solve_captcha(api_key, captcha_file):
    user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=api_key, service_type="rucaptcha").captcha_handler(captcha_file=captcha_file)
    os.remove(f"./{captcha_file}")
    if not user_answer['error']:
        return user_answer['captchaSolve']


async def login(name, password, code, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
        data = {"name": name, "password": password, "captcha": code}
        resp = await session.post(f"{MPETS_URL}/login", data=data)
        await session.close()
        if "Неверная captcha. " in await resp.text():
            return {"status": False,
                    "code": 6,
                    "msg": "Неверная captcha. Неправильное Имя или Пароль"}
        if "Неправильное Имя или Пароль" in await resp.text():
            return {"status": False,
                    "code": 7,
                    "msg": "Incorrect name or password"}
        elif "Ваш питомец заблокирован" in await resp.text():
            return {"status": False,
                    "code": 8,
                    "msg": "This account has blocked"}
        elif "Прочтите, это важно!" in await resp.text():
            resp = await user_agreement(agreement_confirm=True,
                                        params=1,
                                        cookies=cookies,
                                        timeout=timeout,
                                        connector=connector)
            if resp['status'] is True:
                return {"status": True,
                        "name": name,
                        "cookies": cookies}
            else:
                return {"status": False,
                        "code": -1,
                        "msg": f"не удалось принять соглашение {resp['msg']}"}
        elif "Магазин" in await resp.text():
            return {"status": True,
                    "name": name,
                    "cookies": cookies}
    except asyncio.TimeoutError as e:
        return await login(name, password, code, cookies, timeout, connector)
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}
