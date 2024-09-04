from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django_redis import get_redis_connection

from typing import Dict, List, Union
import asyncio

from .forms import LinkForm
from .parser import get_href, get_data, get_download_link
from mycego_test import settings
from .objects.file import File


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
    data: List = request.session.get('data', [])
    try:
        names: List = [item['name'] for item in data]
        paths: List = [item['path'] for item in data]
        sizes: List = [item.get('size', 'None') for item in data]
        types: List = [item['type'] for item in data]
        MIME_types: List = [item.get('mime_type', 'None') for item in data]
        
        download_links: List = await asyncio.gather(
            *(get_download_link(item['public_key'], item['path']) for item in data)
        )    

        files: List = []

        for i in range(len(data)):
            files.append(File(names[i], paths[i], sizes[i], download_links[i], types[i], MIME_types[i]))

        context: Dict = { 'files': files }
        return render(request, 'app/page_for_files.html', context)

    except Exception as e:
        settings.LOGGER.error(f"Error occured, while rendering page for files: {e}  (error)")
        return render(request, 'app/page_for_files.html')  # TODO: Сделать страницу с error или же просто в контекст передать response status и вывести сообщение об этом



    

