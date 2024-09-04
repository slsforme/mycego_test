from django.core.cache import cache

from urllib.parse import urlencode
from typing import Optional, Dict, Any, List
import aiohttp
import asyncio

from mycego_test import settings



async def get_href(disk_link: str) -> Optional[str]:
    """
    
    """
    try:
        api_url: str = "https://cloud-api.yandex.net/v1/disk/public/resources?"
        final_url: str = api_url + urlencode(dict(public_key=disk_link))
        async with aiohttp.ClientSession() as session:
            async with session.get(final_url) as response:
                if response.status == 200:
                    settings.LOGGER.info("Parsed Yandex API with code 200 (info)")
                    data: str = await response.json()
                    if cache.get(disk_link) is None:
                        cache.set(disk_link, data)  # TODO: проверять, есть ли линк в кэше и если что подтягивать оттуда дату
                    return data
                else:
                    settings.LOGGER.error(f"Cannot parse Yandex API for {disk_link}, response code: {response.status} (error)") 
                    return None
    except Exception as e:
        settings.LOGGER.error(f"Error occured while getting response from Yandex API for {disk_link}: {e} (error)")
        return None

async def get_data(data: Dict[str, Any]) -> Optional[List[Dict]]:
    """

    """
    try:
        parsed_items = data.get('_embedded', {}).get('items', [])
        items_list = []
        for _file in parsed_items:
            items_list.append(_file)
        return items_list
    except Exception as e:
        settings.LOGGER.error(f"Error occured while parsing data, gotten from API: {e} (error)")
        return None




