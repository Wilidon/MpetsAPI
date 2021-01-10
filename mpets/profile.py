import asyncio
import re

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def profile(cookies, timeout, connector):
    try:
        club = rank_club = family_id = family_name = club_const = club_day = effect = None
        last_login = "online"
        async with ClientSession(cookies=cookies, timeout=timeout,
                                         connector=connector) as session:
            prof = await session.get("http://mpets.mobi/profile")
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
                    except:
                        last_login = ac.find("span", {'c_red'}).text
                    last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)
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
                    club = ac.text.split(": ")[1].split(",")[0]
                    rank_club = ac.text.split(", ")[1]
                elif 'Верность клубу' in ac.text:
                    club_const = int(ac.text.split(": ")[1].split("%")[0])
                elif 'Дней в клубе:' in ac.text:
                    club_day = int(ac.text.split(": ")[1].replace('\t', ''))
                elif 'Дней в игре:' in ac.text:
                    day = int(ac.text.split(": ")[1].replace('\t', ''))
                elif 'Монеты:' in ac.text:
                    coins = int(ac.text.split(": ")[1].replace('\t', ''))
                elif 'Сердечки:' in ac.text:
                    hearts = int(ac.text.split(": ")[1].replace('\t', ''))
                i += 1
            await session.close()
            return {'status': 'ok',
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
                    'club': club,
                    'rank': rank_club,
                    'club_const': club_const,
                    'club_day': club_day,
                    'day': day}
    except asyncio.TimeoutError as e:
        return {'status': 'error', 'code': '', 'msg': e}
    except Exception as e:
        return {'status': 'error', 'code': '', 'msg': e}


async def view_profile(pet_id, cookies, connector):
    try:
        club_id = club = rank_club = family_id = family_name = club_const = club_day = effect = None
        last_login = 'online'
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                         connector=connector) as session:
            params = {'pet_id': pet_id}
            prof = await session.get("http://mpets.mobi/view_profile", params=params)
            prof = BeautifulSoup(await prof.read(), "lxml")
            ava_id = prof.find('img', {'class': 'ava_prof'})['src'].split("avatar")[1].split(".")[0]
            name = prof.find("div", {"class": "stat_item"}).text.split(", ")[0].replace('\n', '').split(" ", maxsplit=1)[1]
            level = prof.find("div", {"class": "stat_item"}).text.split(", ")[1].split(" ")[0]
            rank = prof.find("div", {"class": "left font_14 pet_profile_stat"}).find_all("div", {"class": "stat_item"})
            for ac in rank:
                if 'Посл. вход:' in ac.text:
                    try:
                        last_login = ac.find("span", {''}).text
                    except:
                        last_login = ac.find("span", {'c_red'}).text
                    last_login = re.sub("^\s+|\n|\r|\s+$", '', last_login)
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
                    club_day = int(ac.text.split(": ")[1].replace('\t', ''))
                elif 'Дней в игре:' in ac.text:
                    day = int(ac.text.split(": ")[1].replace('\t', ''))
            return {'status': 'ok',
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
        return {'status': 'error', 'code': '', 'msg': e}
    except Exception:
        return {'status': 'error',
                'code': 12,
                'msg': 'Failed to get profile'}


async def chest(cookies):
    pass


async def view_posters(cookies):
    pass


async def post_message(pet_id, message, gift_id, cookies, connector):
    pass