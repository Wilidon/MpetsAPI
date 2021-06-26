from loguru import logger
from .utils.trace import request_tracer
import json
from aiohttp import ClientSession
import requests_async as requests


class FastClick(Exception):
    def __init__(self, text):
        self.txt = text


MPETS_URL = "https://mpets.mobi/"


def check_result(method_name: str, content_type: str, status_code: int, body: str):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
    - The server returned an HTTP response code other than 200
    - The content of the result is invalid JSON.
    - The method call was unsuccessful (The JSON 'ok' field equals False)
    :param method_name: The name of the method called
    :param status_code: status code
    :param content_type: content type of result
    :param body: result body
    :return: The result parsed to a JSON dictionary
    :raises ApiException: if one of the above listed cases is applicable
    """
    logger.debug(f'Ответ метода %s: [%d] "%r"', method_name, status_code, body)
    if "Игровой чат" in body:
        raise FastClick("Вы кликаете очень быстро")
    return True


async def make_get_request(method, cookies, timeout, connector):
    logger.debug(f"Запрос на {method}")
    url = f"{MPETS_URL}{method}"
    trace = {}
    try:
        async with ClientSession(timeout=timeout,
                                 connector=connector,
                                 cookies=cookies,
                                 trace_configs=[request_tracer(trace)]) as session:
            try:
                async with session.get(url) as response:
                    if check_result(url, response.content_type, response.status, await response.text()):
                        return await response.text(), trace
            except FastClick:
                return await make_get_request(method, cookies, timeout, connector)
    except Exception as e:
        raise e


async def make_post_request(url, cookies, timeout, connector):
    logger.debug('Запрос на: "%s" с данными: "%r"', method, data)
    try:
        async with session.post(url, data=req, **kwargs) as response:
            return response.content_type, response.status, await response.text()
    except Exception as e:
        raise e
