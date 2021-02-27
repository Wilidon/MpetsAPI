from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from mpets.utils.constants import MPETS_URL


async def threads(forum_id, page, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": forum_id, "page": page}
            resp = await session.get(f"{MPETS_URL}/threads", params=params)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await threads(forum_id, page, cookies,
                                     timeout, connector)
            resp = BeautifulSoup(await resp.read(), "lxml")
            links = []
        for link in resp.find_all("a", href=True):
            a = link["href"]
            links.append(str(a))
        links = [i.split("=")[1] for i in links if "thread?id" in i]
        links = [i.rsplit("&")[0] for i in links]
        if links:
            return {"status": True,
                    "threads": links}
        else:
            # TODO
            return {"status": False,
                    "code": 15,
                    "msg": "На форуме нет топиков."}
    except Exception as e:
        return {'status': False,
                'code': 0,
                'msg': e}


async def thread(thread_id, page, cookies, timeout, connector):
    try:
        moderator_id, moderator_name = None, None
        thread_status, messages = "Открыт", []
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id, "page": page}
            resp = await session.get(f"{MPETS_URL}/thread", params=params)
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread(thread_id, page, cookies,
                                    timeout, connector)
            elif "Сообщений нет" in resp_text:
                return {"status": False,
                        "code": 0,
                        "msg": "Сообщений нет."}
            elif "Форум/Топик не найден или был удален" in resp_text:
                return {"status": False,
                        "code": 0,
                        "msg": "Форум/Топик не найден или был удален."}
            for a in range(len(resp.find_all("div", {"class": "thread_title"}))):
                thread_name = resp.find("div", {"class": "ttl lgreen mrg_ttl mt10"})
                thread_name = thread_name.find("div", {"class": "tc"}).next_element
                pet_id = resp.find_all("div", {"class": "thread_title"})[a]
                pet_id = pet_id.find("a", {"class": "orange_dark2"})["href"].split("=")[1]
                name = resp.find_all("div", {"class": "thread_title"})[a]
                name = name.find("a", {"class": "orange_dark2"}).next_element
                message = resp.find_all("div", {"class": "thread_content"})[a].get_text()
                post_date = resp.find_all("div", {"class": "thread_title"})[a]
                post_date = post_date.find("span", {"class": "post_date nowrap"}).next_element
                message_id = (15 * (int(page) - 1)) + a + 1
                message = dict(pet_id=int(pet_id), name=name,
                               message_id=message_id,
                               message=message, post_date=post_date)
                messages.append(message)
            if "закрыл(а) топик" in resp_text:
                thread_status = "Закрыт"
                moderator_id = resp.find("div",
                                         {"class": "msg mrg_msg1 mt5 c_brown3"})
                moderator_id = moderator_id.find("a", {"class": "pet_name"})
                moderator_id = moderator_id["href"].split("=")[1]
                moderator_id = int(moderator_id)
                moderator_name = resp.find("div",
                                           {"class": "msg mrg_msg1 mt5 c_brown3"})
                moderator_name = moderator_name.find("a", {"class": "pet_name"}).text
            elif "Топик закрыт" in resp_text:
                thread_status = "Закрыт системой."
            return {"status": True,
                    "thread_id": thread_id,
                    "thread_name": thread_name,
                    "page": page,
                    "messages": messages,
                    "thread_status": thread_status,
                    "moderator_id": moderator_id,
                    "moderator_name": moderator_name
                    }
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def add_thread(forum_id, thread_name, thread_text, club_only,
                     cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            data = {"thread_name": thread_name, "forum_id": forum_id,
                    "thread_text": thread_text, "club_only": club_only}
            resp = await session.post(f"{MPETS_URL}/create_thread", data=data)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await add_thread(forum_id, thread_name, thread_text,
                                        club_only, cookies, timeout, connector)
            elif "thread?id=" in str(resp.url):
                thread_id = str(resp.url).split("=")[1].split("&")[0]
                return {"status": True,
                        "thread_id": thread_id,
                        "thread_name": thread_name,
                        "thread_text": thread_text}
            elif "Не удалось cоздать топик" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Не удалось создать топик"}
            elif "Вы не являетесь участником клуба" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Вы не являетесь участником клуба"}
            elif "Заголовок должен быть от 2 до 24 символов" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Заголовок должен быть от 2 до 24 символов"}
            elif "Содержание от 2 до 2500" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Содержание должно быть от 2 до 2500"}
            elif "Вы сможете создавать топики" in await resp.text():
                return {"status": False,
                        "code": 0,
                        "msg": "Вы сможете создавать топики начиная с 18 уровня!"}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "thread_id": thread_id,
                "msg": e}


async def add_vote(forum_id, thread_name, thread_text, vote1,
                   vote2, vote3, vote4, vote5, club_only, cookies,
                   timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            data = {"thread_name": thread_name, "forum_id": forum_id, "thread_text": thread_text,
                    "club_only": club_only, "vote1": vote1, "vote2": vote2, "vote3": vote3,
                    "vote4": vote4, "vote5": vote5, "vote": ""}
            resp = await session.post(f"{MPETS_URL}/create_thread", data=data)
            await session.close()
            if vote1:
                if "thread?id=" in str(resp.url):
                    thread_id = str(resp.url).split("=")[1].split("&")[0]
                    return {"status": True,
                            "thread_id": thread_id,
                            "thread_name": thread_name,
                            "thread_text": thread_text,
                            "vote1": vote1,
                            "vote2": vote2,
                            "vote3": vote3,
                            "vote4": vote4,
                            "vote5": vote5}
                elif "Вы кликаете слишком быстро." in await resp.text():
                    return await add_vote(forum_id, thread_name, thread_text, vote1, vote2, vote3,
                                          vote4, vote5, club_only, cookies, timeout, connector)
                elif "Не удалось cоздать топик" in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Не удалось создать топик"}
                elif "Вы не являетесь участником клуба" in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Вы не являетесь участником клуба"}
                elif "Вы сможете создавать топики" in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Вы сможете создавать топики начиная с 18 уровня!"}
                elif "Заголовок должен быть от 2 до 24 символов" in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Заголовок должен быть от 2 до 24 символов"}
                elif "Содержание от 2 до 2500" in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Содержание должно быть от 2 до 2500"}
                elif "Необходимо указать хотя бы один вариант опроса." in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Необходимо указать хотя бы один вариант опроса."}
                elif "Вариант должен быть от 2 до 24 символов" in await resp.text():
                    return {"status": False,
                            "code": 0,
                            "msg": "Вариант должен быть от 2 до 24 символов"}
            else:
                return {"status": False,
                        "code": 100,
                        "msg": "Incorrect args"}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def thread_message(thread_id, message, cookies, timeout, connector):
    try:
        if 1 < len(str(message)) < 2501:
            async with ClientSession(cookies=cookies, timeout=timeout,
                                     connector=connector) as session:
                data = {"message_text": message, "thread_id": thread_id}
                resp = await session.post(f"{MPETS_URL}/thread_message", data=data)
                await session.close()
                if "thread?id=" in await resp.text():
                    return {"status": True}
                else:
                    return {"status": False,
                            "code": 0,
                            "msg": "Форум/Топик не найден или был удален."}
        else:
            return {"status": False,
                    "code": 0,
                    "msg": "Сообщение должно быть от 2 до 2500 символов"}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def thread_vote(thread_id, vote, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"vote_thread_id": thread_id, "vote_forum_id": 3, "vote": vote}
            await session.get(f"{MPETS_URL}/thread_vote", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def message_edit(message_id, thread_id, message, cookies, timeout, connector):
    # TODO return post_edit_date
    try:
        if 1 < len(message) < 2501:
            async with ClientSession(cookies=cookies, timeout=timeout,
                                     connector=connector) as session:
                data = {"message_id": message_id, "thread_id": thread_id,
                        "page": 1, "message_text": message}
                await session.post(f"{MPETS_URL}/update_message", data=data)
                await session.close()
                return {"status": True}
        else:
            return {"status": False,
                    "code": 0,
                    "msg": "Сообщение должно быть от 2 до 2500 символов"}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def message_delete(message_id, thread_id, page, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": message_id, "page": page, "thread": thread_id}
            await session.get(f"{MPETS_URL}/message_delete", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def delete_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id, "confirm": 1, "clear": 1}
            await session.get(f"{MPETS_URL}/delete_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def edit_thread(thread_name, forum_id, thread_id,
                      thread_text, club_only, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            data = {"thread_name": thread_name, "forum_id": forum_id, "thread_id": thread_id,
                    "first_message_id": 1, "thread_text": thread_text, "club_only": club_only}
            await session.post(f"{MPETS_URL}/update_thread", data=data)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def edit_vote(forum_id, thread_id, thread_name, thread_text,
                    vote1, vote2, vote3, vote4, vote5,
                    club_only, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            data = {"thread_name": thread_name, "forum_id": forum_id, "thread_id": thread_id,
                    "first_message_id": 1, "thread_text": thread_text, "club_only": club_only,
                    "vote1": vote1, "vote2": vote2, "vote3": vote3,
                    "vote4": vote4, "vote5": vote5, "vote": ""}
            r = await session.post(f"{MPETS_URL}/update_thread", data=data)
            await session.close()
            return {"status": True}
    except Exception as e:
        return {"status": False,
                "code": 0,
                "msg": e}


async def restore_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get(f"{MPETS_URL}/restore_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def save_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get(f"{MPETS_URL}/save_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def unsave_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get(f"{MPETS_URL}/unsave_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def close_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get(f"{MPETS_URL}/close_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def open_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get(f"{MPETS_URL}/open_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def attach_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get(f"{MPETS_URL}/attach_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}


async def detach_thread(thread_id, cookies, timeout, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=timeout,
                                 connector=connector) as session:
            params = {"id": thread_id}
            await session.get("http://mpets.mobi/detach_thread", params=params)
            await session.close()
            return {"status": True}
    except Exception as e:
        # TODO
        return {"status": False,
                "code": 0,
                "msg": e}
