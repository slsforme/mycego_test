from django.core.cache import cache

from urllib.parse import urlencode
from typing import Optional, Dict, Any, List, Callable
import aiohttp
import asyncio

from mycego_test import settings
from .handlers import exception_handler, requests_handler


@exception_handler("Error occured while getting response from Yandex Disk API")
async def get_href(disk_link: str) -> Optional[str]:
    """
    
    """
    if cache.get(disk_link) is not None:
        return cache.get(disk_link)
    else:
        api_url: str = "https://cloud-api.yandex.net/v1/disk/public/resources?"
        final_url: str = api_url + urlencode(dict(public_key=disk_link))    
        data: str = await requests_handler(final_url, ['Parsed Yandex API with code 200', f'Cannot parse Yandex Disk API for {disk_link}'])
        cache.set(disk_link, data) 
        return data


@exception_handler("Error occured while getting download link from Yandex Disk API")
async def get_download_link(public_key: str, path: Optional[str] = None) -> Optional[str]:
    """

    """
    api_url: str = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
    params: Dict = { 'public_key': public_key }
    if path is not None:
        params['path'] = path
    final_url: str = api_url + urlencode(params)
    data: str = await requests_handler(final_url, ['Got download link from Yandex Disk API with code 200', 'Cannot get download link for file from Yandex Disk API'])
    return data


@exception_handler("Error occured while parsing data, which were gotten from Yandex Disk API")
async def get_data(data: Dict[str, Any]) -> Optional[List[Dict]]:
    """

    """
    parsed_items = data.get('_embedded', {}).get('items', [])
    return [item for item in parsed_items]



