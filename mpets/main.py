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
                        elif "Вы кликаете слишком быстро." in await resp.text():
                            await session.get(f"{MPETS_URL}/show")
                            await asyncio.sleep(0.4)
                        else:
                            break
                resp = await wakeup(cookies, timeout, connector)
                if resp["status"] is False:
                    await wakeup(cookies, timeout, connector)
            await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def action(action_type, rand, cookies, timeout, connector):
    pass


async def show(cookies, timeout, connector):
    pass


async def wakeup_sleep_info(cookies, timeout, connector):
    pass


async def wakeup_sleep(cookies, timeout, connector):
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


async def charm(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            resp = await session.get("http://mpets.mobi/charm")
            await session.close()
            task = False
            if "Вы кликаете слишком быстро." in await resp.text():
                return await charm(cookies, timeout, connector)
            elif "Результаты" in await resp.text():
                if "Прогресс 2 из 2" in await resp.text():
                    task = False
                elif "Проведи 2 игры в снежки" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
            elif "В очереди" in await resp.text():
                return {"status": True,
                        "queue": True,
                        "game": False,
                        "task": task}
            elif "Снежный бой начинается!" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            elif "выбил Вас" in await resp.text() or "бросил в Вас" in await \
                    resp.text() or "Уворот" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            else:
                if "Проведи 2 игры в снежки" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
    except:
        return {"status": "error"}


async def charm_in_queue(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"in_queue": 1}
            await session.get("http://mpets.mobi/charm", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def charm_out_queue(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"out_queue": 1}
            await session.get("http://mpets.mobi/charm", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def charm_attack(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"attack": 1, "r": 224}
            await session.get("http://mpets.mobi/charm", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def charm_change(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"change": 1, "r": 224}
            await session.get("http://mpets.mobi/charm", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def charm_dodge(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"dodge": 1, "r": 224}
            await session.get("http://mpets.mobi/charm", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def races(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            resp = await session.get("http://mpets.mobi/races")
            await session.close()
            task = False
            if "Вы кликаете слишком быстро." in await resp.text():
                return await races(cookies, timeout, connector)
            elif "Результаты" in await resp.text():
                if "Прогресс 2 из 2" in await resp.text():
                    task = False
                elif "Стань призером скачек 2 раза" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
            elif "В очереди" in await resp.text():
                return {"status": True,
                        "queue": True,
                        "game": False,
                        "task": task}
            elif "Заезд начинается!" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            elif "Сменить" in await resp.text() and "Толкнуть" in await \
                    resp.text() and "Бежать" in await resp.text():
                return {"status": True,
                        "queue": False,
                        "game": True,
                        "task": task}
            else:
                if "Стань призером скачек 2 раза" in await resp.text():
                    task = True
                return {"status": True,
                        "queue": False,
                        "game": False,
                        "task": task}
    except:
        return {"status": "error"}


async def races_in_queue(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"in_queue": 1}
            await session.get("http://mpets.mobi/races", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def races_out_queue(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"out_queue": 1}
            await session.get("http://mpets.mobi/races", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def races_go(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"go": 1, "r": 224}
            await session.get("http://mpets.mobi/races", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def races_attack(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"attack": 0, "r": 224}
            await session.get("http://mpets.mobi/races", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


async def races_change(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"change": 1, "r": 224}
            await session.get("http://mpets.mobi/races", params=params)
            await session.close()
            return {"status": True}
    except:
        return {"status": "error"}


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
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            left_time, travel_status, ids, records = 0, False, [], []
            resp = await session.get(f"{MPETS_URL}/travel")
            await session.close()
            response = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро" in await resp.text():
                return await travel(cookies, timeout, connector)
            if "Ваш питомец гуляет" in await resp.text():
                travel_status = True
                left_time = response.find("span", {"class": "green_dark"}).text.split("осталось ")[1]
            elif "Прогулка завершена!" in await resp.text():
                return await travel(cookies, timeout, connector)
            elif "Рекорд за сутки" in await resp.text():
                travel_ids = response.find("div", {"class": "travel"})
                for link in travel_ids.find_all("a", href=True):
                    ids.append(int(link["href"].split("=")[1]))
                records_list = response.find("table", {"class": "travel_records"})
                nick = records_list.find_all("td", {"class": "cntr td_un"})
                coins = records_list.find_all("td", {"class": "td_r"})
                for i in range(3):
                    records.append({"pet_id": int(nick[i].find("a")["href"].split("=")[1]),
                                    "name": nick[i].text,
                                    "coins": int(coins[i].text)})
            return {"status": True,
                    "travel": travel_status,
                    "left_time": left_time,
                    "ids": ids,
                    "records": records}
    except Exception as e:
        return {"status": False, "code": 0, "msg": e}


async def go_travel(travel_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {"id": travel_id}
            await session.get("http://mpets.mobi/go_travel",
                              params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False, "code": 0, "msg": ""}


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


async def task(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            tasks_list = []
            resp = await session.get(f"{MPETS_URL}/task")
            await session.close()
            resp = BeautifulSoup(await resp.read(), "lxml")
            tasks = resp.find_all("div", {"class": "wr_c3 m-3"})
            for task in tasks:
                task_id = 0
                status = False
                if "Забрать награду" in task.text:
                    status = True
                    task_id = task.find("div", {"class": "span3"})
                    task_id = int(task_id.find("a")["href"].split("=")[1])
                name = task.find("div", {"class": "tc"}).text
                desc = task.find("div", {"class": "mt7 font_13"}).text
                progress = task.find("span", {"class": "c_gray"}).text.split(": ")[1].split(" из ")
                progress = [int(i) for i in progress]
                reward = None
                tasks_list.append({"status": status,
                                   "name": name,
                                   "description": desc,
                                   "progress": progress,
                                   "reward": reward,
                                   "id": task_id})
            return {"status": True,
                    "tasks": tasks_list}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def task_reward(task_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            params = {"id": task_id}
            await session.get(f"{MPETS_URL}/task_reward", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def items(category, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            params = {"category": category}
            if category == "home":
                pass
            elif category == "effect":
                resp = await session.get("http://mpets.mobi/items",
                                         params=params)
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await items(category, cookies, timeout, connector)
                resp = BeautifulSoup(await resp.read(), "lxml")
                effects = resp.find_all("div", {"class": "shop_item"})
                if len(effects) == 1:
                    if "VIP-аккаунт" in effects[0].text:
                        if "Осталось" in effects[0].text:
                            left_time = \
                                effects[0].find("div", {"class": "succes "
                                                                 "mt3"}).text.split(
                                    "Осталось: ")[1]
                            return {"status": True,
                                    "effect": "VIP",
                                    "left_time": left_time}
                        return {"status": True,
                                "effect": "None"}
                elif len(effects) == 2:
                    for effect in effects:
                        if "Премиум-аккаунт" in effect.text:
                            if "Осталось" in effect.text:
                                left_time = effect.find("div", {
                                    "class": "succes mt3"}).text.split(
                                    "Осталось: ")[1]
                                return {"status": True,
                                        "effect": "premium",
                                        "left_time": left_time}
                        if "VIP-аккаунт" in effect.text:
                            return {"status": True,
                                    "effect": "None"}
            elif category == "food":
                pass
            elif category == "play":
                pass

    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def buy(category, item_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            params = {"category": category, "id": item_id}
            if category == "home":
                pass
            elif category == "effect":
                resp = await session.get("http://mpets.mobi/buy",
                                         params=params)
                return {"status": True}
            elif category == "food":
                pass
            elif category == "play":
                pass
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


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
                pet_id = pet.find("a", {"class": "c_brown3"})["href"]
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


async def game_time(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            resp = await session.get(f"{MPETS_URL}/main")
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await game_time(cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div", {"class": "small mt20 mb20 c_lbrown cntr td_un"})
            time = resp.find("div", {"class": "mt5 mb5"}).text.split(", ")[1].split("\n")[0]
            return {"status": True,
                    "time": time}
    except Exception as e:
        return {"status": "error",
                "code": 0,
                "msg": e}


async def items_effect_vip(cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {"category": "effect", "id": 2}
            await session.post("http://mpets.mobi/buy", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": ""}
