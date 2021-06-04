import asyncio
import re
import traceback

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from mpets.utils.constants import MPETS_URL


async def profile(pet_id, cookies, timeout, connector, count=1):
    try:
        club = rank_club = family_id = family_name = club_const = club_day = effect = None
        last_login = "online"
        beauty = coins = hearts = day = 0
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        prof = await session.get("http://mpets.mobi/profile")
        await session.close()
        if "Вы кликаете слишком быстро." in await prof.text():
            return profile(pet_id, cookies, timeout, connector)
        prof = BeautifulSoup(await prof.read(), 'lxml')
        ava_id = prof.find('img', {'class': 'ava_prof'})['src'].split("avatar")[1].split(".")[0]
        name = prof.find("div", {"class": "stat_item"}).text.split(", ")[0].replace(' ', '')
        level = prof.find("div", {"class": "stat_item"})
        level = level.find("a", {"class": "darkgreen_link", "href": "/avatars"})
        level = int(level.next_element.next_element.split(", ")[1].split(" ")[0])
        rank = prof.find("div", {"class": "left font_14 pet_profile_stat"}).find_all("div",
                                                                                     {"class": "stat_item"})
        i = 0
        for ac in rank:
            if 'Посл. вход:' in ac.text:
                try:
                    last_login = ac.find("span", {''}).text
                except Exception:
                    last_login = ac.find("span", {'c_red'}).text
                last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)  # noqa
            elif 'VIP-аккаунт' in ac.text:
                effect = ac.text.split(": ")[1].rsplit('  ', maxsplit=1)[0]
            elif 'Премиум-аккаунт' in ac.text:
                effect = ac.text.split(": ")[1].rsplit(' ', maxsplit=1)[0]
            elif 'Семья' in ac.text:
                family_id = int(ac.find("a", {'darkgreen_link'})['href'].split("=")[1])
                family_name = ac.find("a", {'darkgreen_link'}).text
            elif 'Красота' in ac.text:
                beauty = int(ac.text.split(": ")[1])
            elif 'Клуб:' in ac.text:
                club_id = int(ac.find("a", {'class': 'darkgreen_link'})['href'].split("=")[1])
                club = ac.text.split(": ")[1].split(",")[0]
                rank_club = ac.text.split(", ")[1]
            elif 'Верность клубу' in ac.text:
                club_const = int(ac.text.split(": ")[1].split("%")[0])
            elif 'Дней в клубе:' in ac.text:
                club_day = ac.text.split(": ")[1]
                club_day = int(club_day.split(" ")[0].replace('\t', ''))
            elif 'Дней в игре:' in ac.text:
                day = int(ac.text.split(": ")[1].replace('\t', ''))
            elif 'Монеты:' in ac.text:
                coins = int(ac.text.split(": ")[1].replace('\t', ''))
            elif 'Сердечки:' in ac.text:
                hearts = int(ac.text.split(": ")[1].replace('\t', ''))
            i += 1
        return {'status': True,
                'pet_id': pet_id,
                'name': name,
                'level': level,
                'ava_id': ava_id,
                'last_login': last_login,
                'effect': effect,
                'beauty': beauty,
                'coins': coins,
                'hearts': hearts,
                'family_id': family_id,
                'family_name': family_name,
                'club_id': club_id,
                'club': club,
                'rank': rank_club,
                'club_const': club_const,
                'club_day': club_day,
                'day': day}
    except asyncio.TimeoutError as e:
        if count >= 3:
            return {'status': False, 'code': 1, 'msg': e}
        await profile(pet_id, cookies, timeout, connector, count + 1)
    except Exception as e:
        return {'status': False, 'code': '', 'msg': traceback.print_exc()}


async def view_profile(pet_id, cookies, timeout, connector):
    try:
        club_id = club = rank_club = family_id = family_name = club_const = club_day = effect = None
        last_login = "online"
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"pet_id": pet_id}
            resp = await session.get(f"{MPETS_URL}/view_profile", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await view_profile(pet_id, cookies,
                                          timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            ava_id = resp.find('img', {'class': 'ava_prof'})['src'].split("avatar")[1].split(".")[0]
            ava_id = int(ava_id)
            name = \
                resp.find("div", {"class": "stat_item"}).text.split(", ")[0].replace('\n', '').split(" ", maxsplit=1)[1]
            level = resp.find("div", {"class": "stat_item"}).text.split(", ")[1].split(" ")[0]
            level = int(level)
            rank = resp.find("div", {"class": "left font_14 pet_profile_stat"}).find_all("div", {"class": "stat_item"})
            for ac in rank:
                if 'Посл. вход:' in ac.text:
                    try:
                        last_login = ac.find("span", {''}).text
                    except:
                        last_login = ac.find("span", {'c_red'}).text
                    last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)  # noqa
                elif 'VIP-аккаунт' in ac.text:
                    effect = 'VIP'
                elif 'Премиум-аккаунт' in ac.text:
                    effect = 'premium'
                elif 'Семья' in ac.text:
                    family_id = int(ac.find("a", {'darkgreen_link'})['href'].split("=")[1])
                    family_name = ac.find("a", {'darkgreen_link'}).text
                elif 'Красота' in ac.text:
                    beauty = int(ac.text.split(": ")[1])
                elif 'Клуб:' in ac.text:
                    club_id = int(ac.find("a", {'class': 'darkgreen_link'})['href'].split("=")[1])
                    club = ac.text.split(": ")[1].split(",")[0]
                    rank_club = ac.text.split(", ")[1]
                elif 'Верность клубу' in ac.text:
                    club_const = int(ac.text.split(": ")[1].split("%")[0])
                elif 'Дней в клубе:' in ac.text:
                    club_day = ac.text.split(": ")[1]
                    club_day = int(club_day.split(" ")[0].replace('\t', ''))
                elif 'Дней в игре:' in ac.text:
                    day = int(ac.text.split(": ")[1].replace('\t', ''))
            return {'status': True,
                    'pet_id': pet_id,
                    'name': name,
                    'ava_id': ava_id,
                    'level': level,
                    'last_login': last_login,
                    'effect': effect,
                    'beauty': beauty,
                    'family_id': family_id,
                    'family_name': family_name,
                    'club_id': club_id,
                    'club': club,
                    'rank': rank_club,
                    'club_const': club_const,
                    'club_day': club_day,
                    'day': day}
    except asyncio.TimeoutError as e:
        return {'status': False,
                'code': 1,
                'msg': e}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def chest(cookies, timeout, connector):
    try:
        items = []
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        resp = await session.get(f"{MPETS_URL}/chest")
        await session.close()
        if "Вы кликаете слишком быстро." in await resp.text():
            return await chest(cookies, timeout, connector)
        resp = BeautifulSoup(await resp.read(), 'lxml')
        if "В шкафу пусто" in resp.text:
            return {"status": True,
                    "items": items}
        chest_items = resp.find_all('div', {'class': 'item'})
        for item in chest_items:
            if "Стальной ключ" in item.text:
                type = "key"
                item_id = item.find("a")['href'].split("=")[1]
                if "&" in item_id:
                    item_id = item_id.split("&")[0]
                item_id = int(item_id)
                items.append({"type": type,
                              "item_id": item_id})
            if "Стальной сундук" in item.text:
                type = "chest"
                item_id = item.find("a")['href'].split("=")[1]
                if "&" in item_id:
                    item_id = item_id.split("&")[0]
                item_id = int(item_id)
                timeout = item.find("span", {"class": "succes"}).text.split(" ")[2]
                # timeout = int(timeout)
                items.append({"type": type,
                              "item_id": item_id,
                              "timeout": timeout})
            if "Надеть" in item.text:
                type = "cloth"
                item_id = item.find("span", {"class": "nowrap"})
                item_id = item_id.find("a")['href'].split("=")[1]
                if "&" in item_id:
                    item_id = item_id.split("&")[0]
                item_id = int(item_id)
                items.append({"type": type,
                              "item_id": item_id,
                              "wear_item": True})
            else:
                if "Продать" in item.text:
                    type = "cloth"
                    item_id = item.find("span", {"class": "nowrap"})
                    item_id = item_id.find("a")['href'].split("=")[1]
                    if "&" in item_id:
                        item_id = item_id.split("&")[0]
                    item_id = int(item_id)
                    items.append({"type": type,
                                  "item_id": item_id,
                                  "wear_item": False})
        return {"status": True,
                "items": items}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def wear_item(item_id, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        params = {"id": item_id, "type": "cloth", "back": "chest"}
        await session.get(f"{MPETS_URL}/wear_item", params=params)
        await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def sell_item(item_id, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        params = {"id": item_id, "type": "cloth", "back": "chest"}
        await session.get(f"{MPETS_URL}/sell_item", params=params)
        await session.close()
        return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def view_posters(cookies):
    pass


async def post_message(pet_id, message, gift_id, cookies, connector):
    pass
