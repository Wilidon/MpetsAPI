from mpetsapi import authorization, forum, main, profile, club


class MpetsApi:
    def __init__(self, name=None, password=False, cookies=None, pet_id=None, connector=None):
        self.name = name
        self.password = password
        self.connector = connector

    '''
        Модуль: authorization.py
    '''

    async def start(self, name="standard", password=False, type=1):
        """ Регистрация питомца

            Args:
                name (str): Имя аккаунта (default: стандартный);
                password (str): Пароль аккаунта (default: генерируется 10-значный);
                type (int): Тип аватарки (default: 1).

            Resp:
                pet_id (int): id аккаунта;
                name (str): Имя аккаунта;
                password (str): Пароль от аккаунта;
                cookies (dict): Куки.
        """
        resp = await authorization.start(name=name, password=password, type=type, connector=self.connector)
        if resp['status'] == 'ok':
            self.cookies = resp['cookies']
            self.pet_id = resp['pet_id']
        return resp

    async def login(self):
        """ Авторизация

            Resp:
                cookies (dict): Куки
        """
        resp = await authorization.login(name=self.name, password=self.password, connector=self.connector)
        if resp['status'] == 'ok':
            self.cookies = resp['cookies']
            self.pet_id = resp['pet_id']
        return resp

    '''
        Модуль: main.py
    '''

    async def actions(self):
        """ Три раза кормит, играет и ходит на выставку
        """
        return await main.actions(cookies=self.cookies, connector=self.connector)

    async def wakeup_sleep_info(self):
        pass
        # return action.wakeup_sleep_info(cookies=cookies)

    async def wakeup_sleep(self):
        pass
        # return action.wakeup_sleep(cookies=cookies)'''

    async def wakeup(self):
        """ Дает витаминку за 5 сердец и пропускает минутный сон
        """
        return main.wakeup(cookies=self.cookies, connector=self.connector)

    async def charm(self):
        """ Возвращает данные

        """
        return await main.charm(self.cookies, self.connector)

    async def charm_in_queue(self):
        """ Встать в очередь в снежках

        """
        return await main.charm_in_queue(self.cookies, self.connector)

    async def charm_out_queue(self):
        """ Покинуть очередь в снежках
        """
        return await main.charm_out_queue(self.cookies, self.connector)

    async def charm_attack(self):
        """ Бросить снежок
        """
        return await main.charm_attack(self.cookies, self.connector)

    async def charm_change(self):
        pass

    async def charm_dodge(self):
        pass

    async def races(self):
        pass

    async def races_in_queue(self):
        pass

    async def races_out_queue(self):
        pass

    async def races_go(self):
        pass

    async def races_attack(self):
        pass

    async def races_change(self):
        pass

    async def glade(self):
        """ Поляна

           Resp:
               status (str): статус запроса;
       """

    async def glade_dig(self):
        """ Копать

           Resp:
               status (str): статус запроса;
        """
        return await main.glade_dig(self.cookies, self.connector)

    async def travel(self):
        pass

    async def go_travel(self, travel_id):
        pass

    async def train(self):
        pass

    async def train_skill(self, skill):
        pass

    async def assistants(self):
        pass

    async def assistants_train(self, type):
        pass

    async def jewels(self):
        pass

    async def collect_jewel(self, jewel_id):
        pass

    async def home(self):
        pass

    async def garden(self):
        pass

    async def garden_collect(self, garden_id):
        pass

    async def task(self):
        pass

    async def task_reward(self, task_id):
        pass

    async def items(self, category):
        return await main.items_effect_vip(cookies=self.cookies, connector=self.connector)

    async def buy(self, category, item_id):
        pass

    async def best(self, type, page):
        pass

    async def search_pet(self, name):
        """ Поиск питомца

           Args:
               name (str): имя аккаунта.

           Resp:
               status (str): статус запроса;
               pet_id (int): id аккаунта;
               name (str): имя аккаунта;
               account_status (str): информация о бане.
       """
        return await main.search_pet(name, self.cookies, self.connector)

    async def search_club(self, name):
        pass

    async def show_coin(self):
        pass

    async def show_coin_get(self):
        pass

    async def online(self):
        pass

    async def game_time(self):
        pass

    '''
        Модуль: forum.py
    '''

    async def threads(self, forum_id, page):
        """ Получить список топов

            Args:
                forum_id (int): id форума;
                page (int): страница форума.

            Resp:
                status (str): Статус запроса;
                threads (array): id топиков;
        """
        return await forum.threads(forum_id=forum_id, page=page,
                                   cookies=self.cookies, connector=self.connector)

    async def thread(self, thread_id, page):
        """ Получить содержимое топа

            Args:
                thread_id (int): id топика;
                page (int): страница форума.

            Resp:
                status (str): Статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                page (str): страница топа;
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
        return await forum.thread(thread_id=thread_id, page=page,
                                  cookies=self.cookies, connector=self.connector)

    async def add_thread(self, forum_id, thread_name, thread_text, club_only='on'):
        """ Создает топик

            Args:
                forum_id (int): id форума;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (str): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа.
        """
        return await forum.add_thread(forum_id=forum_id, thread_name=thread_name, thread_text=thread_text,
                                      club_only=club_only, cookies=self.cookies, connector=self.connector)

    async def add_vote(self, forum_id, thread_name, thread_text, vote1,
                       vote2='', vote3='', vote4='', vote5='', club_only='on'):
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
                status (str): статус запроса;
                thread_id (int): id топа;
                thread_name (str): заголовок топа;
                thread_text (str): описание топа.
        """
        return await forum.add_vote(forum_id=forum_id, thread_name=thread_name, thread_text=thread_text,
                                    vote1=vote1, vote2=vote2, vote3=vote3, vote4=vote4, vote5=vote5,
                                    club_only=club_only, cookies=self.cookies, connector=self.connector)

    async def thread_message(self, thread_id, message):
        """ Отправить сообщение

            Args:
                thread_id (int): id топа;
                message (str): сообщение.

            Resp:
                status (str): статус запроса.
        """
        return await forum.thread_message(thread_id=thread_id, message=message,
                                          cookies=self.cookies, connector=self.connector)

    async def send_message(self, thread_id, message):
        """ Аналог метода thread_message()
        """
        return await forum.thread_message(thread_id=thread_id, message=message,
                                          cookies=self.cookies, connector=self.connector)

    async def thread_vote(self, thread_id, vote):
        return await forum.thread_vote(thread_id=thread_id, vote=vote,
                                       cookies=self.cookies, connector=self.connector)

    async def message_edit(self, message_id, thread_id, message):
        """ Отредактировать сообщение

            Args:
                message_id (int): id сообщения;
                thread_id (int): id топа;
                message (str): сообщение.

            Resp:
                status (str): статус запроса.
        """
        return await forum.message_edit(message_id=message_id, thread_id=thread_id, message=message,
                                        cookies=self.cookies, connector=self.connector)

    async def message_delete(self, message_id, thread_id=3):
        """ Удалить сообщение

            Args:
                message_id (int): id сообщения;
                thread_id (int): id топа.

            Resp:
                status (str): статус запроса.
        """
        return await forum.message_delete(message_id=message_id, thread_id=thread_id,
                                          cookies=self.cookies, connector=self.connector)

    async def edit_thread(self, thread_name, forum_id, thread_id, thread_text, club_only='on'):
        """ Отредактировать топ

            Args:
                thread_name (int): заголовок топа;
                forum_id (int): id форума;
                thread_id (int): id топа;
                thread_text (str): описание топа;
                club_only (str): виден ли топ другим (default: on).

            Resp:
                status (str): статус запроса.
        """
        return await forum.edit_thread(thread_name=thread_name, forum_id=forum_id, thread_id=thread_id,
                                       thread_text=thread_text, club_only=club_only,
                                       cookies=self.cookies, connector=self.connector)

    async def delete_thread(self, thread_id):
        """ Удалить топик

            Args:
                thread_id (int): id топа.

            Resp:
                status (str): статус запроса.
        """
        return await forum.delete_thread(thread_id=thread_id, cookies=self.cookies, connector=self.connector)

    async def restore_thread(self, thread_id):
        """ Восстановить топик

            Args:
                thread_id (int): id топа.

            Resp:
                status (str): статус запроса.
        """
        return await forum.restore_thread(thread_id=thread_id, cookies=self.cookies, connector=self.connector)

    async def save_thread(self, thread_id):
        """ Защитить от очистки

            Args:
                thread_id (int): id топа.

            Resp:
                status (str): статус запроса.
       """
        return await forum.save_thread(thread_id=thread_id, cookies=self.cookies, connector=self.connector)

    async def unsave_thread(self, thread_id):
        """ Снять защиту от очистки

            Args:
                thread_id (int): id топа.

           Resp:
                status (str): статус запроса.
       """
        return await forum.unsave_thread(thread_id, self.cookies, self.connector)

    async def close_thread(self, thread_id):
        """ Закрыть топик

           Args:
               thread_id (int): id топа.

           Resp:
               status (str): статус запроса.
       """
        return await forum.close_thread(thread_id, self.cookies, self.connector)

    async def open_thread(self, thread_id):
        """ Открыть топик

           Args:
                thread_id (int): id топа.

           Resp:
                status (str): статус запроса.
       """
        return await forum.open_thread(thread_id, self.cookies, self.connector)

    async def attach_thread(self, thread_id):
        """ Прикрепить топик

           Args:
                thread_id (int): id топа.

           Resp:
                status (str): статус запроса.
       """
        return await forum.attach_thread(thread_id, self.cookies, self.connector)

    async def detach_thread(self, thread_id):
        """ Открепить топик

           Args:
               thread_id (int): id топа.

           Resp:
               status (str): статус запроса.
        """
        return await forum.detach_thread(thread_id, self.cookies, self.connector)

    '''
    club.py
    '''

    async def club(self, club_id=None, page=1):
        """ Получить информацию о клубе

           Args:
                club_id (int): id клуба. без аргумента вернет информацию о своем клубе, либо о приглашении в клуб.

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
        return await club.club(club_id, page, self.cookies, self.connector)

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
        return await club.enter_club(club_id, decline, self.cookies, self.connector)

    async def create_club(self, name):
        return await club.create_club(name, self.cookies, self.connector)

    async def builds(self, club_id):
        return await club.builds(club_id, self.cookies, self.connector)

    async def club_budget(self, club_id):
        return await club.club_budget(club_id, self.cookies, self.connector)

    async def club_budget_history(self, club_id, sort=1, page=1):
        return await club.club_budget_history(club_id, sort, page, self.cookies, self.connector)

    async def club_budget_history_all(self, club_id, sort=1, page=1):
        return await club.club_budget_history_all(club_id, sort, page, self.cookies, self.connector)

    async def leave(self, cookies):
        return await club.leave(cookies=cookies)

    '''
    profile
    '''

    async def profile(self):
        return await profile.profile(self.cookies, self.connector)

    async def view_profile(self, pet_id):
        return await profile.view_profile(pet_id, self.cookies, self.connector)

    async def view_posters(self):
        pass

    async def post_message(self, pet_id, message, gift_id=None):
        return await profile.post_message(pet_id, message, self.cookies, self.connector)