import asyncio
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from mpets.utils.constants import MPETS_URL


async def user_agreement(agreement_confirm, params, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        data = {"agreement_confirm": agreement_confirm,
                "params": params}
        resp = await session.post(f"{MPETS_URL}/user_agreement", data=data)
        await session.close()
        if resp.status == 200:
            return {"status": True}
        else:
            return {"status": False,
                    "code": -1,
                    "msg": "another status code"}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def actions(amount, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        for a in range(amount):
            for b in range(5):
                resp = await session.get(f"{MPETS_URL}/?action=food&rand=1")
                if "Разбудить за" in await resp.text() or "Играть ещё" in await resp.text():
                    await session.close()
                    return {"status": True, "play": False}
                await session.get(f"{MPETS_URL}/?action=play&rand=1")
            while True:
                resp = await session.get(f"{MPETS_URL}/show")
                await asyncio.sleep(0.1)
                if "Соревноваться" in await resp.text():
                    await session.get(f"{MPETS_URL}/show")
                elif "Вы кликаете слишком быстро." in await resp.text():
                    await session.get(f"{MPETS_URL}/show")
                    await asyncio.sleep(1)
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
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        resp = await session.get(f"{MPETS_URL}/?action={action_type}&rand={rand}")
        await session.close()
        if "Разбудить за" in await resp.text() or "Играть ещё" in await resp.text():
            return {"status": True, "play": False}
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def show(cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        while True:
            resp = await session.get(f"{MPETS_URL}/show")
            await asyncio.sleep(0.4)
            if "Соревноваться" in await resp.text():
                await session.get(f"{MPETS_URL}/show")
            elif "Вы кликаете слишком быстро." in await resp.text():
                await session.get(f"{MPETS_URL}/show")
                await asyncio.sleep(0.4)
            else:
                break
        await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def wakeup_sleep_info(cookies, timeout, connector):
    pass


async def wakeup_sleep(cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        await session.get(f"{MPETS_URL}/wakeup_sleep")
        await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def wakeup(cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
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
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        await session.get(f"{MPETS_URL}/glade_dig")
        # await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def travel(cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
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
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
        params = {"id": travel_id}
        await session.get(f"{MPETS_URL}/go_travel",
                          params=params)
        await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False, "code": 0, "msg": e}


async def train(cookies, connector):
    pass


async def train_skill(skill, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
        params = {"skill": skill}
        await session.get(f"{MPETS_URL}/train_skill",
                          params=params)
        await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False, "code": 0, "msg": e}


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
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
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
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
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
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
        params = {"category": category}
        if category == "home":
            pass
        elif category == "effect":
            resp = await session.get("http://mpets.mobi/items",
                                     params=params)
            await session.close()
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
            resp = await session.get("http://mpets.mobi/items",
                                     params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await items(category, cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            shop_item = resp.find("div", {"class": "shop_item"})
            name = shop_item.find("span", {"class": "disabled"}).text
            beauty = shop_item.find("img", {"src": "/view/image/icons/beauty.png"}).next_element.split(" ")[0]
            exp = shop_item.find("img", {"src": "/view/image/icons/expirience.png"}).next_element.split(" ")[0]
            heart = shop_item.find("img", {"src": "/view/image/icons/heart.png"}).next_element.split(" ")[0]
            if "Купить за" in shop_item.text:
                item_id = shop_item.find("a")['href'].split("id=")[1].split("&")[0]
                item_id = int(item_id)
                can_buy = True
                coins = shop_item.find("span", {"class": "bc plr5"}).text.split("за ")[1]
                coins = int(coins)
            elif "требуется" in shop_item.text:
                item_id = shop_item.find("a")['href'].split("id=")[1].split("&")[0]
                item_id = int(item_id)
                item_id = 0
                can_buy = False
            return {"status": True,
                    "name": name,
                    "beauty": beauty,
                    "exp": exp,
                    "heart": heart,
                    "can_buy": False if 'can_buy' not in locals() else can_buy,
                    "item_id": 0 if 'item_id' not in locals() else item_id,
                    "coins": 0 if 'coins' not in locals() else coins,
                    }
        elif category == "play":
            resp = await session.get("http://mpets.mobi/items",
                                     params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await items(category, cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            shop_item = resp.find("div", {"class": "shop_item"})
            name = shop_item.find("span", {"class": "disabled"}).text
            beauty = shop_item.find("img", {"src": "/view/image/icons/beauty.png"}).next_element.split(" ")[0]
            beauty = int(beauty)
            exp = shop_item.find("img", {"src": "/view/image/icons/expirience.png"}).next_element.split(" ")[0]
            exp = int(exp)
            heart = shop_item.find("img", {"src": "/view/image/icons/heart.png"}).next_element.split(" ")[0]
            heart = int(heart)
            if "Купить за" in shop_item.text:
                item_id = shop_item.find("a")['href'].split("id=")[1].split("&")[0]
                item_id = int(item_id)
                can_buy = True
                coins = shop_item.find("span", {"class": "bc plr5"}).text.split("за ")[1]
                coins = int(coins)
            elif "требуется" in shop_item.text:
                item_id = shop_item.find("a")['href'].split("id=")[1].split("&")[0]
                item_id = int(item_id)
                item_id = 0
                can_buy = False
            return {"status": True,
                    "name": name,
                    "beauty": beauty,
                    "exp": exp,
                    "heart": heart,
                    "can_buy": False if 'can_buy' not in locals() else can_buy,
                    "item_id": 0 if 'item_id' not in locals() else item_id,
                    "coins": coins,
                    }

    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def buy(category, item_id, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
        params = {"category": category, "id": item_id}
        if category == "home":
            pass
        elif category == "effect":
            await session.get("http://mpets.mobi/buy",
                              params=params)
            await session.close()
            return {"status": True}
        elif category == "food":
            await session.get("http://mpets.mobi/buy",
                              params=params)
            await session.close()
            return {"status": True}
        elif category == "play":
            await session.get("http://mpets.mobi/buy",
                              params=params)
            await session.close()
            return {"status": True}
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
            class_style = "players tlist font_14 td_un"
            if type == 'club':
                class_style = "players ib tlist font_14"
            resp = resp.find("table", {"class": class_style})
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


async def buy_heart(heart, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        params = {"heart": heart}
        resp = await session.get(f"{MPETS_URL}/buy_heart", params=params)
        await session.close()
        return {"status": True}
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
            if "view_profile" in str(resp.url):
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


async def show_coin_get(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            resp = await session.get(f"{MPETS_URL}/show_coin_get")
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await show_coin_get(cookies, timeout, connector)
            return {"status": True}
    except Exception as e:
        return {"status": "error",
                "code": 0,
                "msg": e}


async def online(page, cookies, timeout, connector):
    try:
        def has_class(tag):
            return not tag.has_attr("class")

        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"page": page}
            pets = []
            resp = await session.get("http://mpets.mobi/online", params=params)
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await online(page, cookies, timeout, connector)
            elif "Список пуст" in await resp.text():
                return {"status": True,
                        "page": page,
                        "pets": pets}
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("table", {"class": "tlist mt5 mb10"})
            resp = resp.find_all(has_class, recursive=False)
            for pet in resp:
                pet_id = pet.find("a", {"class": "c_brown3"})['href']
                pet_id = int(pet_id.split("id=")[1])
                name = pet.find("a", {"class": "c_brown3"}).text
                beauty = int(pet.find("td", {"class": "cntr"}).text)
                pets.append({"pet_id": pet_id,
                             "name": name,
                             "score": beauty})
            return {"status": True,
                    "page": page,
                    "pets": pets}
    except asyncio.exceptions.TimeoutError as e:
        return await online(page, cookies, timeout, connector)
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


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


async def gold_chest(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            resp = await session.get(f"{MPETS_URL}/gold_chest")
            await session.close()
            if "Вы кликаете слишком быстро" in await resp.text():
                return await gold_chest(cookies, timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            keys = resp.find("div", {"class": "mb5 cntr small"}).text
            keys = keys.split("с ")[1].split(" ")[0]
            rewards = []
            players = resp.find("table", {"class": "travel_records"})
            players = players.find_all("tr", {"class": ""})
            for player in players:
                pet_id = player.find("a")['href'].split("=")[1]
                name = player.find("a").text
                reward = player.find("td", {"class": "td_r"}).text.split(" ", maxsplit=1)[1]
                rewards.append({"pet_id": int(pet_id),
                                "name": name,
                                "reward": reward})
            return {"status": True,
                    "amount_keys": int(keys),
                    "rewards": rewards}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def open_gold_chest(cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            resp = await session.get(f"{MPETS_URL}/gold_chest/open")
            resp = BeautifulSoup(await resp.read(), "lxml")
            chest = resp.find("div", {"class": "lplate mt10"})
            found = chest.find("div", {"class": "c_green mt3"}).text
            await session.close()
            return {"status": True,
                    "found": found}
    except Exception as e:
        return {"status": "error",
                "code": 0,
                "msg": e}


async def check_ban(cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        resp = await session.get(f"{MPETS_URL}/chat")
        await session.close()
        if "На вас наложен бан" in await resp.text() and "осталось" in await resp.text():
            return {"status": True,
                    "ban": True}
        else:
            return {"status": True,
                    "ban": False}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}
