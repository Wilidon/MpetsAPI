import aiohttp
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector
from box import Box
from loguru import logger

from mpets import authorization, forum, main, profile, club
from mpets import models


class MpetsApi:
    def __init__(self, name: str = None, password: str = None,
                 cookies: str = None, timeout: int = 5,
                 connector: dict = None, rucaptcha_api: str = None,
                 fast_mode: bool = True):
        self.pet_id: int = None
        self.name: str = name
        self.password: str = password
        self.cookies = cookies
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.connector: dict = connector
        self.rucaptcha_api: str = rucaptcha_api
        self.captcha_file = None
        fast_mode: bool = fast_mode
        self.beauty: int = None
        self.coin: int = None
        self.heart: int = None

        if fast_mode is False:
            ...

    async def get_cookies(self):
        return self.cookies

    async def check_cookies(self):
        resp = await main.check_cookies(cookies=self.cookies,
                                        timeout=self.timeout,
                                        connector=self.connector)
        return Box(resp)

    async def user_agreement(self, agreement_confirm: bool = True,
                             params: int = 1) -> models.ReturnTrueStatus:
        """Принимает пользовательское соглашение

        Args:
            agreement_confirm (bool, optional): [description]. Defaults to True.
            params (int, optional): [description]. Defaults to 1.

        Returns:
            models.ReturnTrueStatus: [description]
        """
        resp = await main.user_agreement(agreement_confirm=agreement_confirm,
                                         params=params,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def start(self, name: str = "standard",
                    password: str = None,
                    type: int = 1) -> Box:
        """ Регистрация питомца

            Args:
                name (str): имя аккаунта (default: стандартный);
                password (str): пароль аккаунта (default: генерируется 10-значный);
                type (int): тип аватарки (default: 1).

            Resp:
                status (bool): статус запроса;
                pet_id (int): id аккаунта;
                name (str): имя аккаунта;
                password (str): пароль от аккаунта;
                cookies (dict): куки.
        """
        resp = await authorization.start(name=name, password=password,
                                         type=type,
                                         timeout=self.timeout,
                                         connector=self.connector)
        if resp["status"]:
            self.cookies = resp["cookies"]
            self.pet_id = resp["pet_id"]
        return Box(resp)

    async def login(self) -> models.authorization.Login:
        """ Авторизация

            Resp:
                status (bool): статус запроса;
                pet_id (int): id аккаунта;
                name (str): имя аккаунта;
                cookies (dict): куки.
        """
        resp = await authorization.get_captcha(self.timeout,
                                               self.connector)
        if resp["status"]:
            self.cookies = resp["cookies"]
            self.captcha_file = resp["captcha"]
        code = await authorization.solve_captcha(api_key=self.rucaptcha_api,
                                                 captcha_file=self.captcha_file)
        resp = await authorization.login(name=self.name,
                                         password=self.password,
                                         code=code,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def actions(self, amount: int = 3):
        """ Кормит, играет и ходит на выставку
        """
        resp = await main.actions(amount=amount,
                                  cookies=self.cookies,
                                  timeout=self.timeout,
                                  connector=self.connector)
        return Box(resp)

    async def action(self, action: str, rand: int = 1):
        # TODO
        """ Выполняет дейсвтие с питомцем

        Args:
            action (str): вид дейсвтия;
            rand (int): случайное число (default: 1).

        Resp:
            status (bool): статус запроса;
        """
        resp = await main.action(action_type=action, rand=rand,
                                 cookies=self.cookies,
                                 timeout=self.timeout,
                                 connector=self.connector)
        return Box(resp)

    async def show(self):
        # TODO
        """ Выставка
        """
        resp = await main.show(cookies=self.cookies,
                               timeout=self.timeout,
                               connector=self.connector)
        return Box(resp)

    async def wakeup_sleep_info(self):
        # TODO
        """ Информация о состоятии питомца.
        """
        resp = await main.wakeup_sleep_info(cookies=self.cookies,
                                            timeout=self.timeout,
                                            connector=self.connector)
        return Box(resp)

    async def wakeup_sleep(self):
        # TODO
        """ Разбудить питомца
        """
        resp = await main.wakeup_sleep(cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def wakeup(self):
        """ Дает витаминку за 5 сердец и пропускает минутный сон
        """
        resp = await main.wakeup(cookies=self.cookies,
                                 timeout=self.timeout,
                                 connector=self.connector)
        return Box(resp)

    async def check_ban(self):
        """ Проверяет наличие бана на аккаунте
                """
        resp = await main.check_ban(cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def charm(self):
        # TODO
        """ Возвращает данные снежков

        """
        resp = await main.charm(cookies=self.cookies,
                                timeout=self.timeout,
                                connector=self.connector)
        return Box(resp)

    async def charm_in_queue(self):
        # TODO
        """ Встать в очередь в снежках

        """
        resp = await main.charm_in_queue(cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def charm_out_queue(self):
        # TODO
        """ Покинуть очередь в снежках
        """
        resp = await main.charm_out_queue(cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def charm_attack(self):
        # TODO
        """ Бросить снежок
        """
        resp = await main.charm_attack(cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def charm_change(self):
        # TODO
        pass

    async def charm_dodge(self):
        # TODO
        pass

    async def races(self):
        # TODO
        pass

    async def races_in_queue(self):
        # TODO
        pass

    async def races_out_queue(self):
        # TODO
        pass

    async def races_go(self):
        # TODO
        pass

    async def races_attack(self):
        # TODO
        pass

    async def races_change(self):
        # TODO
        pass

    async def glade(self):
        # TODO
        """ Поляна

           Resp:
               status (bool): статус запроса;
       """
        resp = ...
        return Box(resp)

    async def glade_dig(self):
        """ Копать

           Resp:
               status (str): статус запроса;
        """
        resp = await main.glade_dig(cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def travel(self):
        resp = await main.travel(cookies=self.cookies,
                                 timeout=self.timeout,
                                 connector=self.connector)
        return Box(resp)

    async def go_travel(self, travel_id):
        resp = await main.go_travel(travel_id=travel_id,
                                    cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def train(self):
        # TODO
        pass

    async def train_skill(self, skill):
        resp = await main.train_skill(skill=skill,
                                      cookies=self.cookies,
                                      timeout=self.timeout,
                                      connector=self.connector)
        return Box(resp)

    async def assistants(self):
        # TODO
        pass

    async def assistants_train(self, type):
        # TODO
        pass

    async def jewels(self):
        # TODO
        pass

    async def collect_jewel(self, jewel_id):
        # TODO
        pass

    async def home(self):
        # TODO
        pass

    async def garden(self):
        # TODO
        pass

    async def garden_collect(self, garden_id):
        # TODO
        pass

    async def task(self):
        resp = await main.task(cookies=self.cookies,
                               timeout=self.timeout,
                               connector=self.connector)
        return Box(resp)

    async def task_reward(self, task_id):
        resp = await main.task_reward(task_id=task_id,
                                      cookies=self.cookies,
                                      timeout=self.timeout,
                                      connector=self.connector)
        return Box(resp)

    async def items(self, category):
        resp = await main.items(category=category,
                                cookies=self.cookies,
                                timeout=self.timeout,
                                connector=self.connector)
        return Box(resp)

    async def buy(self, category: str, item_id: id):
        resp = await main.buy(category=category,
                              item_id=item_id,
                              cookies=self.cookies,
                              timeout=self.timeout,
                              connector=self.connector)
        return Box(resp)

    async def best(self, type: str = "user", page: int = 1):
        resp = await main.best(type=type,
                               page=page,
                               cookies=self.cookies,
                               timeout=self.timeout,
                               connector=self.connector)
        return Box(resp)

    async def buy_heart(self, heart: int = 100):
        resp = await main.buy_heart(heart=heart,
                                    cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector
                                    )

    async def find_pet(self, name):
        """ Поиск питомца

       Args:
           name (str): имя аккаунта.

       Resp:
           status (bool): статус запроса;
           pet_id (int): id аккаунта;
           name (str): имя аккаунта;
           account_status (str): информация о бане.
        """
        resp = await main.find_pet(name=name,
                                   cookies=self.cookies,
                                   timeout=self.timeout,
                                   connector=self.connector)
        return Box(resp)

    async def find_club(self, name: str):
        # TODO
        """ Поиск клуба

           Args:
               name (str): имя клуба.

           Resp:
               status (bool): статус запроса;
               club_id (int): id клуба;
               name (str): имя клуба;
               account_status (str): информация о бане.
       """
        resp = await main.find_club(name=name,
                                    cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def show_coin(self):
        # TODO i forget what it is for
        pass

    async def show_coin_get(self):
        resp = await main.show_coin_get(cookies=self.cookies,
                                        timeout=self.timeout,
                                        connector=self.connector)
        return Box(resp)

    async def online(self, page=1):
        resp = await main.online(page=page,
                                 cookies=self.cookies,
                                 timeout=self.timeout,
                                 connector=self.connector)

        return Box(resp)

    async def game_time(self):
        resp = await main.game_time(cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)

        return Box(resp)

    '''
        Модуль: forum.py
    '''

    async def threads(self, forum_id: int, page: int = 1):
        # TODO добавить возврат имени топа
        """ Получить список топов

            Args:
                forum_id (int): id форума;
                page (int): страница форума (default: 1).

            Resp:
                status (boolean): статус запроса;
                threads (array (int)): id топиков;
        """
        resp = await forum.threads(forum_id=forum_id,
                                   page=page,
                                   cookies=self.cookies,
                                   timeout=self.timeout,
                                   connector=self.connector)
        return Box(resp)

    async def thread(self, thread_id: int, page: int = 1):
        """ Получить содержимое топа

            Args:
                thread_id (int): id топика;
                page (int): страница форума (default: 1).

            Resp:
                status (boolean): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                page (int): страница топа;
                messages(dict): список сообщений в топе;
                    pet_id (int): id автора сообщения;
                    name (str): ник автора сообщения;
                    message_id (int): порядковый номер сообщения в топе;
                    message (str): текст сообщения;
                    post_date (str): дата сообщения.
                thread_status (str): статус топика (Открыт/Закрыт)
                moderator_id (int): id модератора, если топик закрыт (default: None)
                moderator_name (str): ник модератора, если топик закрыт (default: None)
        """
        resp = await forum.thread(thread_id=thread_id,
                                  page=page,
                                  cookies=self.cookies,
                                  timeout=self.timeout,
                                  connector=self.connector)
        return Box(resp)

    async def add_thread(self, forum_id: int, thread_name: str,
                         thread_text: str, club_only: str = "on"):
        """ Создает топик

            Args:
                forum_id (int): id форума;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (boolean): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа.
        """
        resp = await forum.add_thread(forum_id=forum_id,
                                      thread_name=thread_name,
                                      thread_text=thread_text,
                                      club_only=club_only,
                                      cookies=self.cookies,
                                      timeout=self.timeout,
                                      connector=self.connector)
        if resp is None:
            pass
        else:
            return Box(resp)

    async def add_vote(self, forum_id: int, thread_name: str, thread_text: str,
                       vote1: str, vote2: str = "", vote3: str = "",
                       vote4: str = "", vote5: str = "", club_only: str = "on"):
        """ Создать опрос

            Args:
                forum_id (int): id форума;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа;
                vote1 (str): вариант 1;
                vote2 (str): вариант 2;
                vote3 (str): вариант 3;
                vote4 (str): вариант 4;
                vote5 (str): вариант 5;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (boolean): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа.
                vote1 (str): вариант 1;
                vote2 (str): вариант 2;
                vote3 (str): вариант 3;
                vote4 (str): вариант 4;
                vote5 (str): вариант 5;
        """
        resp = await forum.add_vote(forum_id=forum_id,
                                    thread_name=thread_name,
                                    thread_text=thread_text,
                                    vote1=vote1,
                                    vote2=vote2,
                                    vote3=vote3,
                                    vote4=vote4,
                                    vote5=vote5,
                                    club_only=club_only,
                                    cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def thread_message(self, thread_id: int, message: str):
        """ Отправить сообщение

            Args:
                thread_id (int): id топа;
                message (str): сообщение.

            Resp:
                status (boolean): статус запроса;

        """
        resp = await forum.thread_message(thread_id=thread_id,
                                          message=message,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def send_message(self, thread_id, message):
        """ Аналог метода thread_message()
        """
        resp = await forum.thread_message(thread_id=thread_id,
                                          message=message,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def thread_vote(self, thread_id: int, vote: int):
        resp = await forum.thread_vote(thread_id=thread_id,
                                       vote=vote,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def message_edit(self, message_id: int, thread_id: int = 1):
        """ Отредактировать сообщение

            Args:
                message_id (int): id сообщения;
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """
        resp = await forum.message_edit(message_id=message_id,
                                        thread_id=thread_id,
                                        cookies=self.cookies,
                                        timeout=self.timeout,
                                        connector=self.connector)
        return Box(resp)

    async def message_delete(self, message_id: int, thread_id: int = 1, page: int = 1):
        """ Удалить сообщение

            Args:
                message_id (int): id сообщения;
                thread_id (int): id топа (default: 1);
                page (int): номер страницы топа (default: 1).

            Resp:
                status (boolean): статус запроса.
        """
        resp = await forum.message_delete(message_id=message_id,
                                          thread_id=thread_id,
                                          page=page,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def edit_thread(self, thread_name: str, forum_id, thread_id, thread_text,
                          club_only="on"):
        """ Отредактировать топ

            Args:
                thread_name (str): заголовок топа;
                forum_id (int): id форума;
                thread_id (int): id топа;
                thread_text (str): описание топа;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (boolean): статус запроса.
        """
        resp = await forum.edit_thread(thread_name=thread_name,
                                       forum_id=forum_id, thread_id=thread_id,
                                       thread_text=thread_text,
                                       club_only=club_only,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def edit_vote(self, forum_id: int, thread_id: int, thread_name: str, thread_text: str,
                        vote1: str, vote2: str = "", vote3: str = "",
                        vote4: str = "", vote5: str = "", club_only: str = "on"):
        """

        :param forum_id:
        :param thread_id:
        :param thread_name:
        :param thread_text:
        :param vote1:
        :param vote2:
        :param vote3:
        :param vote4:
        :param vote5:
        :param club_only:
        :return:
        """
        resp = await forum.edit_vote(forum_id=forum_id,
                                     thread_id=thread_id,
                                     thread_name=thread_name,
                                     thread_text=thread_text,
                                     vote1=vote1,
                                     vote2=vote2,
                                     vote3=vote3,
                                     vote4=vote4,
                                     vote5=vote5,
                                     club_only=club_only,
                                     cookies=self.cookies,
                                     timeout=self.timeout,
                                     connector=self.connector)
        return Box(resp)

    async def delete_thread(self, thread_id):
        """ Удалить топик

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """
        resp = await forum.delete_thread(thread_id=thread_id,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def restore_thread(self, thread_id):
        """ Восстановить топик

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
        """
        resp = await forum.restore_thread(thread_id=thread_id,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def save_thread(self, thread_id):
        """ Защитить от очистки

            Args:
                thread_id (int): id топа.

            Resp:
                status (boolean): статус запроса.
       """
        resp = await forum.save_thread(thread_id=thread_id,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def unsave_thread(self, thread_id: int):
        """ Снять защиту от очистки

            Args:
                thread_id (int): id топа.

           Resp:
                status (boolean): статус запроса.
       """
        resp = await forum.unsave_thread(thread_id=thread_id,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def close_thread(self, thread_id: int):
        """ Закрыть топик

           Args:
               thread_id (int): id топа.

           Resp:
               status (boolean): статус запроса.
       """
        resp = await forum.close_thread(thread_id=thread_id,
                                        cookies=self.cookies,
                                        timeout=self.timeout,
                                        connector=self.connector)
        return Box(resp)

    async def open_thread(self, thread_id: int):
        """ Открыть топик

           Args:
                thread_id (int): id топа.

           Resp:
                status (boolean): статус запроса.
       """
        resp = await forum.open_thread(thread_id=thread_id,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def attach_thread(self, thread_id: int):
        """ Прикрепить топик

           Args:
                thread_id (int): id топа.

           Resp:
                status (str): статус запроса.
       """
        resp = await forum.attach_thread(thread_id=thread_id,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def detach_thread(self, thread_id: int):
        """ Открепить топик

           Args:
               thread_id (int): id топа.

           Resp:
               status (boolean): статус запроса.
        """
        resp = await forum.detach_thread(thread_id=thread_id,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    '''
    club.py
    '''

    async def club(self, club_id=None, page=1):
        """ Получить информацию о клубе

           Args:
                club_id (int): id клуба.
                (без аргумента вернет информацию о
                своем клубе, либо о приглашении в клуб)

           Resp:
                status (str): статус запроса;
                club (boolean): True, если клуб существует; False, если клуба нет;
                club_id (int): id клуба;
                club_name (str): название клуба;
                about_club (str): описание клуба (default: None);
                data (str): дата основания;
                level (int): уровень клуба;
                exp_club (dict): опыт клуба;
                    now (str): текущий опыт;
                    need (str): до следующего уровня.
                builds (int): уровень построек;
                budget (dict): копилка;
                    coins (int): монет в копилке (default: None);
                    hearts (int): сердце в копилке (default: None).
                number_players (int): количество игроков;
                players (dict): игроки;
                    pet_id (int): id игрока;
                    name (str): имя игрока;
                    exp (str): опыт игрока;
                    rank (str): ранк игрока.
        """
        resp = await club.club(club_id=club_id,
                               page=page,
                               cookies=self.cookies,
                               timeout=self.timeout,
                               connector=self.connector)
        return Box(resp)

    async def club_want(self):
        """ Кнопка «Хочу в клуб»

        """
        return await club.want(self.cookies, self.connector)

    async def accept_invite(self, club_id):
        """ Принять приглашение от клуба

            Args:
                club_id (int): id клуба.
        """
        return await club.accept_invite(club_id, self.cookies, self.connector)

    async def decline_invite(self, club_id):
        """ Отменить приглашение от клуба

            Args:
                club_id (int): id клуба.
        """
        return await club.decline_invite(club_id, self.cookies, self.connector)

    async def enter_club(self, club_id, decline=False):
        """ Отправить заявку в клуб

            Args:
                club_id (int): id клуба.
        """
        return await club.enter_club(club_id, decline, self.cookies,
                                     self.connector)

    async def create_club(self, name):
        return await club.create_club(name, self.cookies, self.connector)

    async def builds(self, club_id):
        return await club.builds(club_id, self.cookies, self.connector)

    async def club_budget(self, club_id):
        return await club.club_budget(club_id, self.cookies, self.connector)

    async def add_club_budget(self, coin, heart):
        resp = await club.add_club_budget(coin=coin,
                                          heart=heart,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def club_budget_history(self, club_id, sort=1, page=1):
        resp = await club.club_budget_history(club_id=club_id,
                                              sort=sort,
                                              page=page,
                                              cookies=self.cookies,
                                              connector=self.connector)
        return Box(resp)

    async def club_budget_history_all(self, club_id, sort=1, page=1):
        return await club.club_budget_history_all(club_id, sort, page,
                                                  self.cookies, self.connector)

    async def forums(self, club_id):
        resp = await club.forums(club_id=club_id,
                                 cookies=self.cookies,
                                 timeout=self.timeout,
                                 connector=self.connector)
        return Box(resp)

    async def chat(self, club_id=0, page=1):
        resp = await club.chat(club_id=club_id,
                               page=page,
                               cookies=self.cookies,
                               timeout=self.timeout,
                               connector=self.connector)
        return Box(resp)

    async def chat_message(self, club_id, message):
        resp = await club.chat_message(club_id=club_id,
                                       message=message,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def collection_changer(self):
        resp = await club.collection_changer(cookies=self.cookies,
                                             timeout=self.timeout,
                                             connector=self.connector)
        return Box(resp)

    async def reception(self, club_id):
        resp = await club.reception(cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def club_history(self, club_id, type=1, page=1):
        resp = await club.club_history(club_id=club_id,
                                       type=type,
                                       page=page,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector
                                       )
        return Box(resp)

    async def club_hint(self):
        resp = await club.club_hint(cookies=self.cookies,
                                    timeout=self.timeout,
                                    connector=self.connector)
        return Box(resp)

    async def club_settings(self, club_id):
        resp = await club.club_settings(cookies=self.cookies,
                                        timeout=self.timeout,
                                        connector=self.connector)
        return Box(resp)

    async def leave(self, cookies):
        return await club.leave(cookies=cookies)

    '''
    profile
    '''

    async def profile(self):
        resp = await profile.profile(pet_id=self.pet_id,
                                     cookies=self.cookies,
                                     timeout=self.timeout,
                                     connector=self.connector)
        return Box(resp)

    async def view_profile(self, pet_id: int):
        resp = await profile.view_profile(pet_id=pet_id,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def view_anketa(self, pet_id: int):
        resp = await profile.view_anketa(pet_id=pet_id,
                                         cookies=self.cookies,
                                         timeout=self.timeout,
                                         connector=self.connector)
        return Box(resp)

    async def view_gifts(self, pet_id, page=1):
        return await profile.view_gifts(pet_id=pet_id,
                                        page=page,
                                        cookies=self.cookies,
                                        timeout=self.timeout,
                                        connector=self.connector)

    async def view_posters(self):
        resp = await profile.view_posters(cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def post_message(self, pet_id, page=1, ):
        return await profile.post_message(pet_id=pet_id,
                                          page=page,
                                          cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)

    async def chest(self):
        resp = await profile.chest(cookies=self.cookies,
                                   timeout=self.timeout,
                                   connector=self.connector)
        return Box(resp)

    async def wear_item(self, item_id: int):
        resp = await profile.wear_item(item_id=item_id,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def sell_item(self, item_id: int):
        resp = await profile.sell_item(item_id=item_id,
                                       cookies=self.cookies,
                                       timeout=self.timeout,
                                       connector=self.connector)
        return Box(resp)

    async def gold_chest(self):
        resp = await main.gold_chest(cookies=self.cookies,
                                     timeout=self.timeout,
                                     connector=self.connector)
        return Box(resp)

    async def open_gold_chest(self):
        resp = await main.open_gold_chest(cookies=self.cookies,
                                          timeout=self.timeout,
                                          connector=self.connector)
        return Box(resp)

    async def test_proxy(self, ):
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        proxies = {
            'http': 'socks5://176.9.119.170:1080',
            'https': 'socks5://176.9.119.170:1080'
        }
        connector = ProxyConnector.from_url('socks5://127.0.0.1:9050')
        # connector = None
        async with ClientSession(connector=connector) as session:
            r = await session.get("https://api.ipify.org")
            r = await r.text()
            return r
