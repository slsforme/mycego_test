from typing import Callable, Optional, List, Dict, Any

import aiohttp
import asyncio
from urllib.parse import urlencode

from mycego_test import settings


def exception_handler[T](_prompt: str, return_value: Any = None):
    """
    Данная функция является генератором декораторов.
    В неё поступает в виде аргументов _prompt для лога 
    и возвращаемое значение, которое по умолчанию является None.
    Сама функция возвращает декоратор, который оборачивает целевую функцию,
    принимающую в себя любые аргументы и возвращать значения типа T.
    Возвращаемое значение - функция с любыми аргументами и 
    возвращаемым значением T или же None. Сама функция содержится в блоке 
    try... catch с целью обработки всех ошибок, которые могут возникнуть
    при работе данной корутины. В случае ошибки в систему добавляется лог
    и возвращается значение, указанное в аргументах декоратора.

    :param _prompt: prompt для лога
    :param return_value: Возвращаемое значение при ошибке.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        """
        :param func: Функция, которая будет обернута декоратором.
        :type func: Callable[..., T]
        
        :return: Асинхронная обертка, которая выполняет корутину и логирует ошибки.
        :rtype: Callable[..., Optional[T]]
        """
        async def wrapper(*args, **kwargs) -> Optional[T]:     
            """
            :param args: позиционные аргументы
            :param kwargs: именованные аргументы
            :return: Результат выполнения функции или значение по умолчанию в случае ошибки.
            :rtype: T | None 
            """  
            try:
                return await func(*args, **kwargs) 
            except Exception as e:
                settings.LOGGER.error(f"{_prompt}: {e} (error)")
                return return_value
        return wrapper
    return decorator


@exception_handler("Error occurred while handling request")
async def request_handler(url: str, _prompts: List[str], is_text: bool = None) -> Optional[str]:
    """
    Обрабатывает запрос по заданному URL, 
    возвращая текст или JSON в зависимости от параметров.

    :param url: URL, по которому будет отправлен запрос.
    :type url: str
    :param _prompts: список строк для логирования 
    :type _prompts: List[str]
    :param is_text: Флаг, указывающий на то, стоит ли сериализовать 
    дату в json или оставить, как текст. Если None, возвращается JSON.
    :type is_text: bool, None
    :return: Текстовое или JSON представление ответа в 
    случае успешного запроса. 
    В случае же неудачного запроса возвращает None.
    :rtype: str | None
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                settings.LOGGER.info(f"{_prompts[0]} (info)")
                if is_text is True:
                    data: str = await response.text()
                    return data
                data: str = await response.json()
                return data
            else:
                settings.LOGGER.error(f"{_prompts[1]}, response code: {response.status} (error)") 
                return None
                

@exception_handler("Error occurred while building url")
async def url_builder(base_url: str, params: Dict) -> Optional[str]:
    """
    Создаёт URL из базового URL и параметров.
    Для этого просто к базовому URL добавляются
    закодированные параметры.

    :param base_url: Базовый URL, к которому будут добавлены параметры.
    :type base_url: str
    :param params: Словарь параметров, которые будут добавлены к URL.
    :type params: Dict
    :return: Полный URL с параметрами при успешной построении, иначе None.
    :rtype: str | None
    """
    return base_url + urlencode(params)


@exception_handler("Error occurred while extracting field")
async def extract_field(data: List[Dict[str, Any]], key_name: str, default_value: Any = 'None') -> List[Any]:
    """
    Извлекает значения по заданному ключу из списка словарей.

    :param data: Список словарей, из которых извлекаются данные.
    :type data: List[Dict[str, Any]]
    :param key_name: Имя ключа, по которому извлекаются значения.
    :type key_name: str
    :param default_value: Значение по умолчанию, возвращаемое в случае отсутствия ключа.
    :type default_value: Any, str
    :return: Список значений, извлеченных по ключу, или значение по умолчанию, если ключ отсутствует.
    :rtype: List[Any]
    """
    return [item.get(key_name, default_value) for item in data]

