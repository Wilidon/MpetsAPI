import asyncio
from aiohttp import ClientSession, ClientTimeout


async def actions(cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            for a in range(3):
                for b in range(5):
                    await session.get("http://mpets.mobi/?action=food&rand=1")
                    await asyncio.sleep(0.4)
                    await session.get("http://mpets.mobi/?action=play&rand=1")
                    await asyncio.sleep(0.4)
                    while True:
                        r = await session.get('https://mpets.mobi/show')
                        await asyncio.sleep(0.4)
                        if "Соревноваться" in await r.text():
                            await session.get('https://mpets.mobi/show')
                            await asyncio.sleep(0.4)
                        else:
                            break
                await wakeup(cookies, connector)
            await session.close()
        return {'status': 'ok'}
    except Exception as e:
        return {'status': 'error', 'code': 0, 'msg': ''}


def action_food(cookies):
    pass


def action_play(cookies):
    pass


def show(cookies):
    pass


async def wakeup_sleep_info(cookies):
    pass


def wakeup_sleep(cookies):
    pass


async def wakeup(cookies, connector):
    async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                             connector=connector) as session:
        await session.get("http://mpets.mobi/wakeup")
        await session.close()
        return {'status': 'ok'}


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


async def glade_dig(cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            await session.get("http://mpets.mobi/glade_dig")
            await session.close()
            return {'status': 'ok'}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


async def travel(cookies, connector):
    pass


async def go_travel(travel_id, cookies, connector):
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


async def best(type, page, cookies, connector):
    pass


async def search_pet(name, cookies, connector):
    try:
        async with ClientSession(cookies=cookies, timeout=ClientTimeout(total=10),
                                 connector=connector) as session:
            data, account_status = {'name': name}, None
            resp = await session.post("http://mpets.mobi/find_pet", data=data)
            if "Имя должно быть от 3 до 12 символов!" in await resp.text():
                return {'status': 'error', 'code': 0, 'msg': ''}
            elif "Питомец не найден!" in await resp.text():
                return {'status': 'error', 'code': 0, 'msg': ''}
            elif "Игрок заблокирован" in await resp.text():
                account_status = 'block'
            elif "Игрок забанен" in await resp.text():
                account_status = 'ban'
            elif "view_profile" in str(resp.url):
                pet_id = str(resp.url).split("id=")[1].split("&")[0]
            await session.close()
            return {'status': 'ok', 'pet_id': pet_id, 'name': name, 'account_status': account_status}
    except Exception as e:
        # TODO
        return {'status': 'error', 'code': 0, 'msg': ''}


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
