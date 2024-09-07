from django.core.cache import cache

from urllib.parse import urlencode
from typing import Optional, Dict, Any, List, Callable
import aiohttp
import asyncio

from mycego_test import settings
from .handlers import exception_handler, request_handler, url_builder

@exception_handler("Error occurred while getting response from Yandex Disk API")
async def get_href(disk_link: str) -> Optional[str]:
    """
    Данная функция отвечает за получение данных 
    с Yandex Disk API. Если данные уже ранее были кэшированы,
    то они берутся из него по ключу и возвращаются.
    В ином случае, отправляется запрос на endpoint API,
    который в себе содержит public key Яндекс Диска,
    ранее данным пользователем. После получения данных 
    происходит их кэширование, чтобы не отправлять
    лишние запросы к Yandex Disk API и возвращается.

    :param disk_link: Ссылка на Диск пользователя.
    :type disk_link: str
    :return: Метаданные о Диске.
    :rtype: str
    """
    if cache.get(disk_link) is not None:
        settings.LOGGER.info(f"Data was from {disk_link} previously cached. (info)")
        return cache.get(disk_link)
    else:
        final_url = await url_builder('https://cloud-api.yandex.net/v1/disk/public/resources?', dict(public_key=disk_link))
        data: str = await request_handler(final_url, ['Parsed Yandex API with code 200', f'Cannot parse Yandex Disk API for {disk_link}'])
        cache.set(disk_link, data) 
        return data


@exception_handler("Error occurred while getting download link from Yandex Disk API")
async def get_download_link(public_key: str, path: Optional[str] = None) -> str:
    """
    Данная функция отвечает за получение ссылки на скачивание ресурса.
    Сначала проверяется, есть ли в аргументах путь до ресурса,
    если нет, то он просто не включается в параметры запроса.
    В параметры всегда обязательно входит публичный ключ ресурса,
    по которому будет запрошена ссылка на скачивание.
    При успешном запросе возвращается ссылка на скачивание.
    
    :param public_key: Публичный ключ ресурса.
    :type public_key: str  
    :param path: Путь до ресурса внутри Диска.
    :type path: str | None
    :return: Данные с ссылкой для скачивания.
    :rtype: str
    """
    params: Dict = { 'public_key': public_key }
    if path is not None:
        params['path'] = path
    final_url: str = await url_builder('https://cloud-api.yandex.net/v1/disk/public/resources/download?', params)
    data: str = await request_handler(final_url, ['Got download link from Yandex Disk API with code 200', 'Cannot get download link for file from Yandex Disk API'])
    return data


@exception_handler("Error occurred while parsing data, which were gotten from Yandex Disk API")
async def get_data(data: Dict[str, Any]) -> List[Dict]:
    """
    Данная фукнция отвечает за парсинг даты из сериализованного ответа
    от сервера в формате json. По ключу _embedded получаем данные из запроса, 
    из которых извлекаем все ресурсы из Диска по ключу items. 
    В результате возвращается лист с каждым элементом из parsed_items.
    В случае, если данные не удалось получить по данному ключу, 
    возвращается пустой лист или словарь.
    
    :param data: Словарь с данными, полученный с Yandex Disk API.
    :type data: Dict[str, Any]
    :return: Лист со словарями данных, содержащие в себе
     метаданные о файлах.
    :rtype: List[Dict]
    """
    parsed_items = data.get('_embedded', {}).get('items', [])
    return [item for item in parsed_items]



