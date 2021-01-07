from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup


async def threads(forum_id, page, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.get("http://mpets.mobi/threads", params={'id': forum_id, 'page': page})
            await session.close()
            resp = BeautifulSoup(await resp.read(), "lxml")
            links = []
        for link in resp.find_all("a", href=True):
            a = link["href"]
            links.append(str(a))
        links = [i.split('=')[1] for i in links if 'thread?id' in i]
        links = [i.rsplit("&")[0] for i in links]
        if links:
            return {'status': 'ok', 'threads': links}
        else:
            # TODO
            return {'status': 'error', 'code': 15, 'msg': 'Failed to get threads id'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 15, 'msg': 'Failed to get threads id'}


async def thread(thread_id, page, cookies, connector):
    try:
        moderator_id, moderator_name, thread_status, messages = None, None, "Открыт", []
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            resp = await session.get("http://mpets.mobi/thread", params={'id': thread_id, 'page': page})
            await session.close()
            resp_text = await resp.text()
            resp = BeautifulSoup(await resp.read(), "lxml")
            if "Вы кликаете слишком быстро." in resp_text:
                return await thread(thread_id, page, cookies, connector)
            elif "Сообщений нет" in resp_text:
                # TODO
                return {'status': 'error', 'code': 1, 'msg': 'Messages not.'}
            elif "Форум/Топик не найден или был удален" in resp_text:
                # TODO
                return {'status': 'error', 'code': 2, 'msg': 'Thread not exist'}
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
                message = dict(pet_id=pet_id, name=name, message_id=message_id, message=message, post_date=post_date)
                messages.append(message)
            if "закрыл(а) топик" in resp_text:
                thread_status = "Закрыт"
                moderator_id = resp.find("div", {"class": "msg mrg_msg1 mt5 c_brown3"})
                moderator_id = moderator_id.find("a", {"class": "pet_name"})["href"].split("=")[1]
                moderator_name = resp.find("div",
                                           {"class": "msg mrg_msg1 mt5 c_brown3"})
                moderator_name = moderator_name.find("a", {"class": "pet_name"}).text

            if "Топик закрыт" in resp_text:
                thread_status = "Закрыт системой."
            return {'status': 'ok',
                    'thread_id': thread_id,
                    'thread_name': thread_name,
                    'page': page,
                    'messages': messages,
                    'thread_status': thread_status,
                    'moderator_id': moderator_id,
                    'moderator_name': moderator_name
                    }
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def add_thread(forum_id, thread_name, thread_text, club_only, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            data = {'thread_name': thread_name, 'forum_id': forum_id, 'thread_text': thread_text,
                    'club_only': club_only}
            resp = await session.post("http://mpets.mobi/create_thread", data=data)
            await session.close()
            if "Вы кликаете слишком быстро." in await resp.text():
                return await add_thread(forum_id, thread_name, thread_text, club_only, cookies, connector)
            elif "thread?id=" in str(resp.url):
                thread_id = str(resp.url).split("=")[1].split("&")[0]
                return {'status': 'ok', 'thread_id': thread_id, 'thread_name': thread_name, 'thread_text': thread_text}
            elif "Не удалось cоздать топик" in await resp.text():
                return {'status': 'error', 'code': 19, 'msg': 'Failed to create topic'}
            elif "Вы не являетесь участником клуба" in await resp.text():
                return {'status': 'error', 'code': 20,
                        'msg': 'You are not a member of the club and can not create topics here'}
            elif "Вы сможете создавать топики" in await resp.text():
                return {'status': 'error', 'code': 21, 'msg': 'You can create topics starting at level 18!'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def add_vote(forum_id, thread_name, thread_text, vote1, vote2, vote3, vote4, vote5, club_only, cookies,
                   connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            data = {'thread_name': thread_name, 'forum_id': forum_id, 'thread_text': thread_text,
                    'club_only': club_only, 'vote1': vote1, 'vote2': vote2, 'vote3': vote3,
                    'vote4': vote4, 'vote5': vote5, 'vote': ''}
            resp = await session.post("http://mpets.mobi/create_thread", data=data)
            await session.close()
            if vote1:
                if "thread?id=" in str(resp.url):
                    thread_id = str(resp.url).split("=")[1].split("&")[0]
                    return {'status': 'ok', 'thread_id': thread_id, 'thread_name': thread_name,
                            'thread_text': thread_text}
                elif "Вы кликаете слишком быстро." in await resp.text():
                    return await add_vote(forum_id, thread_name, thread_text, vote1, vote2, vote3,
                                          vote4, vote5, club_only, cookies, connector)
                elif "Не удалось cоздать топик" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'Failed to create topic'}
                elif "Вы не являетесь участником клуба" in await resp.text():
                    return {'status': 'error', 'code': 0,
                            'msg': 'You are not a member of the club and can not create topics here'}
                elif "Вы сможете создавать топики" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'You can create topics starting at level 18!'}
                elif "Заголовок должен быть от 2 до 24 символов" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'Заголовок должен быть от 2 до 24 символов'}
                elif "Содержание от 2 до 2500" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'Содержание от 2 до 2500'}
                elif "Необходимо указать хотя бы один вариант опроса." in await resp.text() \
                    or "Вариант должен быть от 2 до 24 символов" in await resp.text():
                    return {'status': 'error', 'code': 0, 'msg': 'Необходимо указать хотя бы один вариант опроса. or '
                                                                 'Вариант должен быть от 2 до 24 символов'}
            else:
                return {'status': 'error', 'code': 100, 'msg': 'Incorrect args'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'thread_id': thread_id, 'msg': 'Failed to get thread'}


async def thread_message(thread_id, message, cookies, connector):
    try:
        if 1 < len(str(message)) < 2501:
            async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                     connector=connector) as session:
                data = {'message_text': message, 'thread_id': thread_id}
                resp = await session.post("http://mpets.mobi/thread_message", data=data)
                await session.close()
                if "thread?id=" in await resp.text():
                    return {'status': 'ok'}
                else:
                    return {'status': 'error', 'code': 0, 'msg': 'Forum/Topic not found or was deleted'}
        else:
            return {'status': 'error', 'code': 0, 'msg': 'The message must be between 2 and 2500 characters long'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': 'The message must be between 2 and 2500 characters long'}


async def thread_vote(thread_id, vote, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'vote_thread_id': thread_id, 'vote_forum_id': 3, 'vote': vote}
            r = await session.get("http://mpets.mobi/thread_vote", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': 'The message must be between 2 and 2500 characters long'}


async def message_edit(message_id, thread_id, message, cookies, connector):
    # TODO return post_edit_date
    try:
        if 1 < len(message) < 2501:
            async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                     connector=connector) as session:
                data = {'message_id': message_id, 'thread_id': thread_id, "page": 1, "message_text": message}
                await session.post("http://mpets.mobi/update_message", data=data)
                await session.close()
                return {'status': 'ok'}
        else:
            return {'status': 'error', 'code': 0, 'msg': 'The message must be between 2 and 2500 characters long'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': 'The message must be between 2 and 2500 characters long'}


async def message_delete(message_id, thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': message_id, 'page': thread_id, 'thread': 733936}
            await session.get("http://mpets.mobi/message_delete", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def delete_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id, 'confirm': 1, 'clear': 1}
            await session.get("http://mpets.mobi/delete_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def edit_thread(thread_name, forum_id, thread_id, thread_text, cookies, club_only, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            data = {'thread_name': thread_name, 'forum_id': forum_id, 'thread_id': thread_id,
                    'first_message_id': 1, 'thread_text': thread_text}
            await session.post("http://mpets.mobi/update_thread", data=data)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def restore_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/restore_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def save_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/save_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def unsave_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/unsave_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def close_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/close_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def open_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/open_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def attach_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/attach_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def detach_thread(thread_id, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            params = {'id': thread_id}
            await session.get("http://mpets.mobi/detach_thread", params=params)
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}
