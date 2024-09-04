from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django_redis import get_redis_connection

from typing import Dict, List, Union
import asyncio

from .forms import LinkForm
from .parser import get_href, get_data
from mycego_test import settings

async def home(request: HttpRequest) -> render or redirect:
    """

    """
    try:
        if request.method == 'POST':
            form = LinkForm(request.POST)
            if form.is_valid():
                link: str = form.cleaned_data["link"]
                data: Union[str, None] = await get_href(link)
                if data is None:
                    form = LinkForm()
                else:
                    data: Union[List, None] = await get_data(data)
                    if data is not None:
                        request.session['data'] = data
                        return redirect('page-for-files')
                    else:
                        form = LinkForm()
        else:
            form = LinkForm()
        context: Dict = {
            'form': form
        }
        return render(request, 'app/index.html', context)
    except Exception as e:
        settings.LOGGER.error(f"Error occured, while rendering home page: {e} (error)")
        return render(request, 'app/index.html')  # TODO: Сделать страницу с error или же просто в контекст передать response status и вывести сообщение об этом


async def page_for_files(request: HttpRequest) -> render:
    """

    """
    try:
        connecion = get_redis_connection('default')
        data = re

        context: Dict = {

        }
        return render(request, 'app/page_for_files.html')
    except Exception as e:
        settings.LOGGER.error(f"Error occured, while rendering page for files: {e} (error)")

    

