from aiohttp import ClientSession, ClientTimeout


async def get_settings_game(cookies, status=None):
    pass


async def set_settings_game(params, cookies):
    pass


async def change_name(name, cookies):
    pass


async def change_pw(password, cookies, timeout, connector):
    try:
        if 3 <= len(password) <= 20:
            async with ClientSession(cookies=cookies, timeout=timeout,
                                     connector=connector) as session:
                data = {'pw': password}
                resp = await session.post("http://mpets.mobi/change_pw", data=data)
                await session.close()
                if "Пароль успешно изменен!" in await resp.text():
                    return {"status": True,
                            "password": password}
                elif "Вы кликаете слишком быстро." in await resp.text():
                    return {"status": True,
                            "password": password}
                else:
                    #TODO error code
                    return {"status": "error",
                            "code": 8,
                            "msg": "error"}
        else:
            return {"status": "error", "code": 7, "msg": "Password must be between 3 and 20 characters"}
    except Exception:
        return {"status": "error", "code": 8, "msg": "erroor"}


async def change_avatars(type, cookies):
    pass


async def set_email(email, cookie):
    pass


async def get_id(cookies):
    pass


async def logout(cookies):
    pass