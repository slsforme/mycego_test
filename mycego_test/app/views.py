from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django_redis import get_redis_connection

from typing import Dict, List, Union, Optional
import asyncio
import aiohttp
import mimetypes
import re
from http import HTTPStatus

from .forms import LinkForm
from .parser import get_href, get_data, get_download_link
from .handlers import request_handler, extract_field, exception_handler
from mycego_test import settings
from .objects.file import File


async def handle_download_links(data: List) -> List:
    """
    Данная функция собирает все ссылки для скачивания 
    при помощи запуска несколько корутин одновременно, 
    в которые передаётся публичный ключ и путь до файла
    внутри диска.

    :param data: данные, полученные с Yandex Disk API.
    :type data: List
    :return: лист с ссылками на скачивание каждого файла из data
    :rtype: List

    """
    return await asyncio.gather(
        *(get_download_link(item['public_key'], item['path']) for item in data)
    )


async def home(request: HttpRequest) -> Union[render, redirect]:
    """
    Данная функция отвечает за обработку представления
    index.html - домашней страницы. В ней инициализируется
    форма, которая при отправке данных на сервер - методе POST
    из представления home-page реализуется валидацию формы
    при помощи регулярного выражения. Если данные проходят валидацию -
    то используя корутину get_href мы получаем ответ от сервера, в 
    котором содержится информация о данном диске. Для того, чтобы
    использовать данные в представлении для показа файлов с диска,
    добавляем их в сессию и редиректим пользователя на данное представлении.

    :param request: запрос со стороны пользователя
    :type request: HttpRequest
    :return: render страницы home или redirect на страницу page-for-files 
    :rtype: render | redirect
    """
    try:
        YANDEX_DISK_PATTERN: str = r'^https:\/\/disk\.yandex\.ru\/d\/[a-zA-Z0-9_-]+$'
        error_message: Optional[str] = None
        if request.method == 'POST':
            form = LinkForm(request.POST)
            if form.is_valid():
                link: str = form.cleaned_data["link"]
                if re.match(YANDEX_DISK_PATTERN, link):
                    data: Union[str, None] = await get_href(link)
                    if data is None:
                        form = LinkForm()
                    else:
                        data: Union[List, None] = await get_data(data)
                        request.session['data'] = data
                        return redirect('page-for-files')
                else:
                    form = LinkForm()
                    error_message = 'Вы неправильно ввели ссылку на Yandex Disk.'
        else:
            form = LinkForm()
            error_message = 'Вы неправильно ввели ссылку на Yandex Disk.'

        return render(request, 'app/index.html', { 'form': form, 'error_message': error_message } )
    except Exception as e:
        settings.LOGGER.error(f"Error occured, while rendering home page: {e} (error)")
        return render(request, 'app/error.html',  { 'status': HTTPStatus.BAD_REQUEST , 'description': HTTPStatus.BAD_REQUEST.description }) 

async def page_for_files(request: HttpRequest) -> render:
    """
    Данная фукнция отвечает за обработку представления page_for_files.html
    В ней из сессии берутся данные, и далее формируются листы из с данными о каждом файле.
    Потом также подтягиваются ссылки для скачивания. 
    После этого формируется лист с объектами типа данных File и передаётся в представление.
    
    :param request: запрос со стороны пользователя
    :type request: HttpRequest
    :return: render страницы page-for-files 
    :rtype: render 
    """
    try:
        data: List = request.session.get('data', [])
        file_metadata: List = [
                *(await asyncio.gather(*[
                    extract_field(data, 'name'),
                    extract_field(data, 'path'),
                    extract_field(data, 'size'),
                    extract_field(data, 'type'),
                    extract_field(data, 'mime_type'),
                ]))
        ]

        download_links: List = await handle_download_links(data)

        files: List = [
                File(file_metadata[0][i], file_metadata[1][i], file_metadata[2][i],
                download_links[i]['href'], file_metadata[3][i], file_metadata[4][i])
                for i in range(len(data))
        ]

        return render(request, 'app/page_for_files.html', { 'files': files } )  
    except Exception as e:
        settings.LOGGER.error(f"Error occured, while rendering page for files: {e} (error)")
        return render(request, 'app/error.html',  { 'status': HTTPStatus.BAD_REQUEST , 'description': HTTPStatus.BAD_REQUEST.description })  

def filtered_page(request: HttpRequest, filter_string: str) -> render:
    """
    Данная фукнция отвечает за 
    фильтрацию файлов в представлении page_for_files.html
    В неё поступает запрос и строка - фильтр. 
    Фильтрация происходит по MIME - типу файла - берём левую часть разделённой строки, 
    хранящей в себе MIME - тип и проводим по ней фильтрацию.

    :param request: запрос со стороны пользователя
    :param filter_string: фильтр
    :type request: HttpRequest
    :type filter_string: str
    :return: render страницы page-for-files 
    :rtype: render 
    """
    try:
        data: List = request.session.get('data', [])

        file_metadata: List = []

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            file_metadata = loop.run_until_complete(asyncio.gather(
                extract_field(data, 'name'),
                extract_field(data, 'path'),
                extract_field(data, 'size'),
                extract_field(data, 'type'),
                extract_field(data, 'mime_type')
            ))
        finally:
            loop.close()

        print(file_metadata)

        download_links: List = asyncio.run(handle_download_links(data))

        files = [
            File(file_metadata[0][i], file_metadata[1][i], file_metadata[2][i], download_links[i]['href'], file_metadata[3][i], file_metadata[4][i])
            for i in range(len(data))
            if file_metadata[4][i].split('/')[0] == filter_string
        ]

        return render(request, 'app/page_for_files.html', { "files": files })
    except Exception as e:
        settings.LOGGER.error(f"Error occured, while rendering home page: {e} (error)")
        return render(request, 'app/error.html',  { 'status': HTTPStatus.BAD_REQUEST , 'description': HTTPStatus.BAD_REQUEST.description })  # TODO: Сделать страницу с error или же просто в контекст передать response status и вывести сообщение об этом


