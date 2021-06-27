import asyncio
import re
import traceback

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from mpets.utils.constants import MPETS_URL


async def profile(pet_id, cookies, timeout, connector, count=1):
    try:
        club_id = club = rank_club = family_id = family_name = club_const = club_day = effect = None
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
            elif 'Красота:' in ac.text:
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
        return {'status': False, 'code': '', 'msg': e}


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
                elif 'Красота:' in ac.text:
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


async def view_posters(cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        params = {"r": 1}
        resp = await session.get(f"{MPETS_URL}/view_posters", params=params)
        await session.close()
        resp = BeautifulSoup(await resp.read(), "lxml")
        players = resp.find_all("div", {"class": "poster mb3"})
        posters = []
        for player in players:
            unread = False
            pet_id = player.find_all("a")[0]['href'].split("=")[1]
            pet_id = int(pet_id)
            name = player.find_all("a")[0].text
            text = player.find_all("a")[1].text.replace("	", "").replace("\r", "").replace("\n", "")
            post_date = player.find("div", {"class": "pl_date"}).text.replace("	", "")
            post_date = post_date.replace("\n\r\n", "").replace("\n", "")
            # Опредлеяем прочитано сообщение или нет
            temp = player.find("div", {"class": "pl_cont"}).find_all("a")[1]['class'][0]
            if temp == 'unread_post':
                unread = True
            posters.append({"pet_id": pet_id,
                            "name": name,
                            "text": text,
                            "post_date": post_date,
                            "unread": unread})
        return {'status': True,
                "players": posters}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def post_message(pet_id, page, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies, timeout=timeout,
                                connector=connector)
        params = {"pet_id": pet_id, "page": page}
        resp = await session.get(f"{MPETS_URL}/post_message", params=params)
        await session.close()
        resp = BeautifulSoup(await resp.read(), "lxml")
        msgs = resp.find_all("div", {"class": "msg mrg_msg1 mt5 c_brown4"})
        messages = []
        for message in msgs:
            pet_id = message.find("a")['href'].split("=")[1]
            pet_id = int(pet_id)
            name = message.find_all("a")[0].text
            text = message.find("div", {"class": "post_content"}).text
            post_date = message.find("span", {"class": "post_date nowrap"}).text.replace("	", "")
            post_date = post_date.replace("\n\r\n", "").replace("\n", "")
            messages.append({"pet_id": pet_id,
                             "name": name,
                             "text": text,
                             "post_date": post_date})
        return {'status': True,
                "messages": messages}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def view_anketa(pet_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=timeout,
                                 connector=connector) as session:
            about = real_name = gender = city = birthday = ank = None
            params = {'pet_id': pet_id}
            resp = await session.get("http://mpets.mobi/view_anketa",
                                     params=params)
            prof = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in await resp.text():
                return await view_anketa(pet_id, cookies, timeout, connector)
            anketa = prof.find_all("span", {"class": "anketa_head ib mb3"})
            for i in range(len(anketa)):
                if "себе" in str(anketa[i].text):
                    about = prof.find_all("div", {"class": "mb10"})[i].text
                elif "Реальное имя" in anketa[i].text:
                    real_name = prof.find_all("div", {"class": "mb10"})[i].text
                elif "Пол" in anketa[i].text:
                    gender = prof.find_all("div", {"class": "mb10"})[i].text
                    gender = gender.replace("\r", "").replace("\n", "")
                    gender = gender.replace("\t", "")
                elif "Город" in anketa[i].text:
                    city = prof.find_all("div", {"class": "mb10"})[i].text
                    city = city.replace("\r\n\r\n\t\t\t", "").replace("\r\n\t\t\t\t\t\t\t\n", "")
                elif "Дата рождения" in anketa[i].text:
                    birthday = prof.find_all("div", {"class": "mb10"})[i].text
                    birthday = birthday.replace("\r\n\t\t\t\t", "").replace("\t\t\t\t\t\t\t", "")
                elif "Анкета" in anketa[i].text:
                    ank = prof.find_all("div", {"class": "mb10"})[i].text
            return {'status': True,
                    'pet_id': int(pet_id),
                    'about': about,
                    'real_name': real_name,
                    'gender': gender,
                    'city': city,
                    'birthday': birthday,
                    'ank': ank}
    except asyncio.TimeoutError as e:
        return await view_anketa(pet_id, cookies, timeout, connector)
    except Exception as e:
        return {'status': False,
                'code': 12,
                'msg': e}


async def view_gifts(pet_id, page, cookies, timeout, connector):
    try:
        session = ClientSession(cookies=cookies,
                                timeout=timeout,
                                connector=connector)
        params = {'pet_id': pet_id, "page": page}
        players = []
        resp = await session.get("http://mpets.mobi/view_gifts",
                                 params=params, cookies=cookies)
        gifts = BeautifulSoup(await resp.read(), "lxml")
        if "Вы кликаете слишком быстро." in await resp.text():
            return await view_gifts(pet_id, page, cookies, timeout, connector)
        items = gifts.find_all('div', {'class': 'item'})
        for item in items:
            name, pet_id = None, None
            present_id = item.find("img", {"class": "item_icon"})["src"]
            present_id = present_id.split("present")[1].split(".")[0]
            pet_id = item.find("a", {"class": "pet_name il"})
            if pet_id:
                name = pet_id.text
                pet_id = pet_id["href"].split("=")[1]
            date = item.find("span", {"class": "gray_color font_13"}).text
            date = date.split("получен")[1]
            # НЕ ДЕЛАЙ БЛЯТЬ PET_ID B PRESENT_ID ЧИСЛОВЫМ ТИПОМ

            # 25.06.2021
            # добавили в уп капчу, половину нормального кода приходится переписыать на быструю руку.
            # короче pet_id в принципе можно сделать интовым, но нужна проверка скрытый подарок или нет
            players.append({"pet_id": pet_id, "name": name,
                            "present_id": present_id, "date": date})
        return {'status': True,
                'page': page,
                'players': players}
    except asyncio.TimeoutError as e:
        return {'status': False, 'code': '', 'msg': e}
    except Exception as e:
        return {'status': False,
                'code': 12,
                'msg': e}


async def post_send(pet_id, message, gift_id, cookies, connector):
    pass
