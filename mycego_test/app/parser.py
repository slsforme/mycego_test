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
async def get_download_link(public_key: str, path: Optional[str] = None) -> Optional[str]:
    """

    """
    params: Dict = { 'public_key': public_key }
    if path is not None:
        params['path'] = path
    final_url: str = await url_builder('https://cloud-api.yandex.net/v1/disk/public/resources/download?', params)
    data: str = await request_handler(final_url, ['Got download link from Yandex Disk API with code 200', 'Cannot get download link for file from Yandex Disk API'])
    return data


@exception_handler("Error occurred while parsing data, which were gotten from Yandex Disk API")
async def get_data(data: Dict[str, Any]) -> Optional[List[Dict]]:
    """

    """
    parsed_items = data.get('_embedded', {}).get('items', [])
    return [item for item in parsed_items]



