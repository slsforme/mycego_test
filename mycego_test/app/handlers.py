from typing import Callable, Optional, List, Dict, Any

import aiohttp
import asyncio
from urllib.parse import urlencode

from mycego_test import settings


def exception_handler[T, P](_prompt: str, return_value: Any = None):
    """

    """
    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        async def wrapper(*args, **kwargs) -> Optional[T]:       
            try:
                return await func(*args, **kwargs) 
            except Exception as e:
                settings.LOGGER.error(f"{_prompt}: {e} (error)")
                return return_value
        return wrapper
    return decorator


async def request_handler(url: str, _prompts: List[str], is_text: bool = None) -> Optional[str]:
    """
    
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

    """
    return base_url + urlencode(params)


@exception_handler("Error occured while extracting field")
async def extract_field(data: List[Dict[str, Any]], key_name: str, default_value: Any = 'None') -> List[Any]:
    return [item.get(key_name, default_value) for item in data]

