from typing import Callable, Optional, List

import aiohttp
import asyncio

from mycego_test import settings


def exception_handler[T, P](_prompt: str):
    """

    """
    def decorator(func: Callable[..., T]) -> Callable[..., Optional[T]]:
        async def wrapper(*args, **kwargs) -> Optional[T]:       
            try:
                return await func(*args, **kwargs) 
            except Exception as e:
                settings.LOGGER.error(f"{_prompt}: {e} (error)")
                return None
        return wrapper
    return decorator


async def requests_handler(url: str, _prompts: List[str]) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                settings.LOGGER.info(f"{_prompts[0]} (info)")
                data: str = await response.json()
                return data
            else:
                settings.LOGGER.error(f"{_prompts[1]}, response code: {response.status} (error)") 
                return None