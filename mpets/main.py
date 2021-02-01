import asyncio
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from mpets.utils.constants import MPETS_URL


async def actions(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            for a in range(3):
                for b in range(5):
                    await session.get(f"{MPETS_URL}/?action=food&rand=1")
                    await asyncio.sleep(0.4)
                    await session.get(f"{MPETS_URL}/?action=play&rand=1")
                    while True:
                        resp = await session.get(f"{MPETS_URL}/show")
                        await asyncio.sleep(0.4)
                        if "Соревноваться" in await resp.text():
                            await session.get(f"{MPETS_URL}/show")
                            await asyncio.sleep(0.4)
                        else:
                            break
                resp = await wakeup(cookies, timeout, connector)
                if resp["status"] is False:
                    await session.close();
                    return resp
            await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


def action(action, rand, cookies, timeout, connector):
    pass


def show(cookies, timeout, connector):
    pass


async def wakeup_sleep_info(cookies, timeout, connector):
    pass


def wakeup_sleep(cookies, timeout, connector):
    pass


async def wakeup(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            await session.get(f"{MPETS_URL}/wakeup")
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def charm(cookies, connector):
    pass


async def charm_in_queue(cookies, connector):
    pass


async def charm_out_queue(cookies, connector):
    pass


async def charm_attack(cookies, coonnector):
    pass


async def charm_change(cookies, connector):
    pass


async def charm_dodge(cookies, connector):
    pass


async def races(cookies, connector):
    pass


async def races_in_queue(cookies, connector):
    pass


async def races_out_queue(cookies, connector):
    pass


async def races_go(cookies, connector):
    pass


async def races_attack(cookies, connector):
    pass


async def races_change(cookies, connector):
    pass


async def glade(cookies, connector):
    pass


async def glade_dig(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            await session.get(f"{MPETS_URL}/glade_dig")
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def travel(cookies, timeout, connector):
    pass


async def go_travel(travel_id, cookies, timeout, connector):
    pass


async def train(cookies, connector):
    pass


async def train_skill(skill, cookies, connector):
    pass


async def assistants(cookies, connector):
    pass


async def assistants_train(type, cookies, connector):
    pass


async def jewels(cookies, connector):
    pass


async def collect_jewel(jewel_id, cookies, connector):
    pass


async def home(cookies, connector):
    pass


async def garden(cookies, connector):
    pass


async def garden_collect(garden_id, cookies, connector):
    pass


async def task(cookies, connector):
    pass


async def task_reward(task_id, cookies, connector):
    pass


async def items(category, cookies, connector):
    pass


async def buy(category, item_id, cookies, connector):
    pass


async def best(type, page, cookies, timeout, connector):
    try:
        def has_class(tag):
            return not tag.has_attr("class")

        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {type: "true", "page": page}
            pets = []
            resp = await session.get(f"{MPETS_URL}/best", params=params)
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await best(type, page, cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("table", {"class": "players tlist font_14 td_un"})
            resp = resp.find_all(has_class, recursive=False)
            for pet in resp:
                place = int(pet.find("td").text)
                pet_id = pet.find("a", {"class": "c_brown3"})['href']
                pet_id = int(pet_id.split("id=")[1])
                name = pet.find("a", {"class": "c_brown3"}).text
                beauty = int(pet.find_all("td")[2].text)
                pets.append({"place": place,
                             "pet_id": pet_id,
                             "name": name,
                             "beauty": beauty})
            return {"status": True,
                    "pets": pets}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def find_pet(name, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            data, account_status = {"name": name}, None
            resp = await session.post(f"{MPETS_URL}/find_pet", data=data)
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await find_pet(name, cookies, timeout, connector)
            elif "Имя должно быть от 3 до 12 символов!" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Имя должно быть от 3 до 13 символов"}
            elif "Питомец не найден!" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Питомец не найден!"}
            elif "Игрок заблокирован" in await resp.text():
                account_status = "block"
            elif "Игрок забанен" in await resp.text():
                account_status = "ban"
            elif "view_profile" in str(resp.url):
                pet_id = str(resp.url).split("id=")[1].split("&")[0]
            return {"status": True,
                    "pet_id": pet_id,
                    "name": name,
                    "account_status": account_status}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def find_club(name, cookies, timeout, connector):
    pass


async def show_coin(cookies, connector):
    pass


async def show_coin_get(cookies, connector):
    pass


async def online(cookies, connector):
    pass


async def game_time(cookies, connector):
    pass


async def items_effect_vip(cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'category': 'effect', 'id': 2}
            await session.post("http://mpets.mobi/buy", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}
