from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from mpets.utils.constants import MPETS_URL


async def club(club_id, page, cookies, timeout, connector):
    try:
        about_club = data = level = exp_club = number_players = builds = None
        players = []
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            if club_id:
                params = {"id": club_id, "page": page}
            else:
                params = {"id": 0}
            club_inf = await session.get(f"{MPETS_URL}/club", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await club_inf.text():
                return await club(club_id, page, cookies, timeout, connector)
            if "?id=" in str(club_inf.url):
                club_id = str(club_inf.url).split("=")[1]
                if "&" in club_id: club_id = club_id.split("&")[0]
                # отдельно, потому что может быть page
                # и проверка условия выше обязательна
                club_id = int(club_id)
                club_inf = BeautifulSoup(await club_inf.read(), "lxml")
                club_name = club_inf.find("div", {"class": "club_title cntr"}).text.replace("\n", "")
                if "Клуб" in club_name:
                    club_name = club_name.rsplit("  ", maxsplit=1)[0].split("Клуб ")[1]
                else:
                    club_name = \
                    club_name.rsplit("  ", maxsplit=1)[0]
                inf = club_inf.find("div", {"class": "wr_c4 left"})
                inf = inf.find_all("span", {"class": "green_dark"})
                if len(inf) == 4:
                    about_club = inf[0].text.split("  ", maxsplit=1)
                    if len(about_club) == 1:
                        about_club = about_club[0].rsplit(" ", maxsplit=1)[0]
                    else:
                        about_club = about_club[1].rsplit(" ", maxsplit=1)[0]
                    data = inf[1].text.split(" ", maxsplit=1)[1]
                    level = int(inf[2].text)
                    exp_club = inf[3].text.replace("\r", "").replace("\n", "")
                    exp_club = exp_club.replace("\t", "").split("из ")
                else:
                    data = inf[0].text.split(" ", maxsplit=1)[1]
                    level = int(inf[1].text)
                    exp_club = inf[2].text.replace("\r", "").replace("\n", "")
                    exp_club = exp_club.replace("\t", "").split("из ")
                try:
                    builds = club_inf.find("div", {"class": "font_15 mb3 mt5"})
                    builds = int(builds.text.split(": ")[1].split(" ")[0])
                except:
                    pass
                number_players = club_inf.find("span", {"class": "club_desc"}).text
                number_players = number_players.replace("\n", "")
                number_players = number_players.split("(")[1].split(")")[0]
                number_players = int(number_players.split(" из ")[0])
                pets = club_inf.find("div", {"class": "blub_list_pets"})
                pets = pets.find_all("span", {"class": ""})
                for pet in pets:
                    pet_id = pet.find("a", {"class": "club_member"})["href"]
                    pet_id = int(pet_id.split("=")[1])
                    name = pet.find("a", {"class": "club_member"}).text
                    exp = pet.text.split(" -")[0].split(" ", maxsplit=1)[1]
                    rank = pet.text.split("- ")[1]
                    players.append({"pet_id": pet_id, "name": name, "exp": exp, "rank": rank})
                return {"status": True,
                        "club": True,
                        "club_id": club_id,
                        "club_name": club_name,
                        "about_club": about_club,
                        "data": data,
                        "level": level,
                        "exp_club": exp_club,
                        "builds": builds,
                        "number_players": number_players,
                        "players": players}
            else:
                await session.close()
                if "Бонусы клуба" in await club_inf.text():
                    club_inf = BeautifulSoup(await club_inf.read(), "lxml")
                    club_inf = club_inf.find("div", {'class': 'wr_c1'})
                    club_name = club_inf.find("b").text
                    club_id = club_inf.find("a", {"class": "darkgreen_link"})['href'].split("=")[1]
                    bonus_heart = club_inf.find_all("span", {"class": "succes"})[0].text.split("+")[1].split("%")[0]
                    bonus_exp = club_inf.find_all("span", {"class": "succes"})[1].text.split("+")[1].split("%")[0]
                    return {"status": True,
                            "club": None,
                            "club_id": club_id,
                            "club_name": club_name,
                            "bonus_heart": bonus_heart,
                            "bonus_exp": bonus_exp}
                else:
                    return {"status": True,
                            "club": None}
    except Exception as e:
        # TODO
        return {"status": True,
                "code": 0,
                "msg": e}


async def want(cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'want': 1}
            await session.get("http://mpets.mobi/clubs", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def accept_invite(club_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': club_id}
            await session.get("http://mpets.mobi/accept_invite", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def decline_invite(club_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': club_id}
            await session.get("http://mpets.mobi/decline_invite", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def enter_club(club_id, decline, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            if decline is False:
                params = {'id': club_id}
                resp = await session.get("http://mpets.mobi/enter_club", params=params)
                await session.close()
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await enter_club(club_id, cookies, connector)
                elif "Заявка успешно отправлена!" in await resp.text():
                    return {'status': 'ok'}
                elif "Вы уже состоите в клубе" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'Вы уже состоите в клубе'}
                elif "Вы уже отправляли в этот клуб заявку" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'Вы уже отправляли в этот клуб заявку'}
                elif "Вы отправляли заявку в клуб" in await resp.text():
                    params = {'id': club_id, 'yes': 1}
                    resp = await session.get("http://mpets.mobi/enter_club", params=params)
                    if "Вы кликаете слишком быстро." in await resp.text():
                        return await enter_club(club_id, cookies, connector)
                    elif "Заявка успешно отправлена!" in await resp.text():
                        return {'status': 'ok'}
                    elif "Вы уже состоите в клубе" in await resp.text():
                        return {'status': 'error', 'code': 0, 'msg': 'Вы уже состоите в клубе'}
                    elif "Вы уже отправляли в этот клуб заявку" in await resp.text():
                        return {'status': 'error', 'code': 0, 'msg': 'Вы уже отправляли в этот клуб заявку'}
            else:
                params = {'id': club_id, 'decline': 1}
                resp = await session.get("http://mpets.mobi/enter_club", params=params)
                await session.close()
                if "Вы кликаете слишком быстро." in await resp.text():
                    return await enter_club(club_id, cookies, connector)
                elif "Заявка отменена!" in await resp.text():
                    return {'status': 'ok'}

    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def create_club(name, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            data = {'name': name}
            resp = await session.post("http://mpets.mobi/create_club", data=data)
            await session.close()
            if "Название клуба должно быть от 2 до 20 символов" in await resp.text():
                return {"status": "error", "code": 0, "msg": "Название клуба должно быть от 2 до 20 символов"}
            elif "Клуб с таким именем уже существует" in await resp.text():
                return {"status": "error", "code": 0, "msg": "Клуб с таким именем уже существует"}
            elif "Неизвестная ошибка, попробуйте позже" in await resp.text():
                return {"status": "error", "code": 0, "msg": "Неизвестная ошибка, попробуйте позже"}
            elif "Вам не хватает " in await resp.text():
                return {"status": "error", "code": 0, "msg": "Вам не хватает монет"}
            elif "Пока вы в клубе, вы не можете создать клуб" in await resp.text():
                return {"status": "error", "code": 0, "msg": "Пока вы в клубе, вы не можете создать клуб"}
            elif "Клуб не найден" in await resp.text():
                return {"status": "error", "code": 0, "msg": "Клуб не найден"}
            elif "Имя клуба не должно содержать символы с направлением письма справа налево" in await resp.text():
                return {"status": "error", "code": 0,
                        "msg": "Имя клуба не должно содержать символы с направлением письма справа налево"}
            elif "Недопустимые символы в названии клуба" in await resp.text():
                return {"status": "error", "code": 0,
                        "msg": "Недопустимые символы в названии клуба"}
            else:
                return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def builds(club_id, cookies, connector):
    pass


async def club_budget(club_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': club_id}
            resp = await session.get("http://mpets.mobi/club_budget", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_budget(club_id, cookies, connector)
            elif "Копилка:" in await resp.text():
                resp = BeautifulSoup(await resp.read(), "lxml")
                coins = resp.find("div", {"class": "cntr"}).find_all("img", {"class": "price_img"})[1].next_element
                hearts = resp.find("div", {"class": "cntr"}).find_all("img", {"class": "price_img"})[2].next_element
                max_coins = resp.find("div", {"class": "p3 left"}).find_all("img", {"class": "price_img"})[0].next_element.split(": ")[1]
            return {'status': 'ok',
                    'coins': coins,
                    'hearts': hearts,
                    'max_coins': max_coins}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def add_club_budget(coin, heart, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            data = {'coin': coin, 'heart': heart}
            await session.post("http://mpets.mobi/add_club_budget", data=data)
            return {"status": "ok"}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def club_budget_history(club_id, sort, page, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': club_id, 'sort': sort, 'page': page}
            players, last_reset_pet_id, last_reset_name = [], None, None
            resp = await session.get("http://mpets.mobi/club_budget_history", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_budget_history(club_id, sort, page, cookies, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            pets = resp.find("div", {"class": "wr_c4 left p10"}).find_all("div", {"class": "td_un"})
            for pet in pets:
                pet_id = int(pet.find("a")['href'].split("=")[1])
                name = pet.find("a").next_element
                count = pet.text.split(": ")[1].replace("\t", "")
                players.append({'pet_id': pet_id, 'name': name, 'count': count})
            resp = resp.find("div", {"class": "msg mrg_msg1 mt10 c_brown4"})
            resp = resp.find("div", {"class": "wr_c4 td_un"})
            last_reset = resp.text.replace("\n", "").replace("\t", "").replace("\r", "").split(": ")[1]
            last_reset = last_reset.split("(")[0]
            try:
                last_reset_pet_id = int(resp.find("a", {"class": "club_member"})['href'].split("=")[1])
                last_reset_name = resp.text.replace("\n", "").replace("\t", "").replace("\r", "").split(": ")[1]
                last_reset_name = last_reset_name.split("(")[1].split(")")[0]
            except Exception as e:
                pass
            return {'status': 'ok',
                    'club_id': club_id,
                    'sort': sort,
                    'page': page,
                    'players': players,
                    'last_reset': last_reset,
                    'last_reset_pet_id': last_reset_pet_id,
                    'last_reset_name': last_reset_name}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def club_budget_history_all(club_id, sort, page, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': club_id, 'sort': sort, 'page': page}
            players = []
            resp = await session.get("http://mpets.mobi/club_budget_history_all", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_budget_history(club_id, sort, page, cookies, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            pets = resp.find("div", {"class": "wr_c4 left p10"}).find_all("div", {'class': 'td_un'})
            for pet in pets:
                pet_id = int(pet.find("a")['href'].split("=")[1])
                name = pet.find("a").next_element
                count = int(pet.text.split(": ")[1].replace('\t', ''))
                players.append({'pet_id': pet_id, 'name': name, 'count': count})
            return {'status': 'ok',
                    'club_id': club_id,
                    'sort': sort,
                    'page': page,
                    'players': players}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def forums(forum_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {'id': forum_id}
            forums_id = []
            resp = await session.get("http://mpets.mobi/forum", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await forums(forum_id, cookies, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            threads = resp.find_all("div", {"class": "mbtn orange"})
            for forum in threads:
                forum_id = int(forum.find("a")['href'].split("=")[1])
                name = forum.text
                forums_id.append(
                    {'forum_id': forum_id, 'name': name})
            return {'status': 'ok',
                    'club_id': forum_id,
                    'forums_id': forums_id}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def chat(club_id, page, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {'id': club_id, 'page': page}
            messages = []
            resp = await session.get(
                "http://mpets.mobi/chat", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await chat(club_id, page, cookies, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            pets = resp.find_all("div", {'class': 'post_chat'})
            for pet in pets:
                pet_id = int(pet.find("a")['href'].split("=")[1])
                name = pet.find("a").next_element
                message = pet.find("span", {"class": "pet_msg"}).text
                messages.append(
                    {'pet_id': pet_id, 'name': name, 'message': message})
            return {'status': 'ok',
                    'club_id': club_id,
                    'page': page,
                    'messages': messages}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def collection_changer(cookies, timeout, connector):
    pass


async def reception(cookies, timeout, connector):
    pass


async def club_history(club_id, type, page, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies,
                                 timeout=ClientTimeout(total=timeout),
                                 connector=connector) as session:
            params = {'id': club_id, 'type': type, 'page': page}
            history = []
            resp = await session.get(
                "http://mpets.mobi/club_history", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await club_history(club_id, type, page, cookies,
                                          timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            resp = resp.find("div", {'class': 'msg mrg_msg1 mt5 c_brown4'})
            resp = resp.find_all("div", {'class': 'mb2'})
            for his in resp:
                try:
                    date = his.find("span", {"class": "c_gray"}).text
                    owner_id = int(his.find("a")["href"].split("=")[1])
                    owner_name = his.find("a").next_element
                    member_id = int(his.find_all("a")[1]["href"].split("=")[1])
                    member_name = his.find_all("a")[1].next_element
                    action = his.find_all("span")[1].text
                    history.append(
                        {'owner_id': owner_id,
                         'owner_name': owner_name,
                         'member_id': member_id,
                         'member_name': member_name,
                         'action': action,
                         'date': date})
                except:
                    pass
            return {'status': 'ok',
                    'club_id': club_id,
                    'page': page,
                    'history': history}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def club_hint(cookies, timeout, connector):
    pass


async def club_settings(cookies, timeout, connector):
    pass


async def gerb(cookies, timeout, connector):
    pass


async def club_about(cookies, timeout, connector):
    pass


async def club_about_action(cookies, timeout, connector):
    pass


async def club_rename(cookies, timeout, connector):
    pass


async def club_rename_action(cookies, timeout, connector):
    pass


async def leave_club(cookies, timeout, connector):
    try:
        pass
    except Exception as e:
        return {'status': 'error',
                'code': '',
                'msg': ''}