from typing import Optional, Any
from mycego_test import settings

class File():
    """
    Объект File представляет собой ресурс с метаданными и ссылкой для скачивания.

    Атрибуты:
        name (str): Имя ресурса.
        path (str): Путь к ресурсу.
        size (Optional[int]): Размер ресурса в байтах. Может быть None, если данный ресурс - папка.
        type (str): Тип ресурса - файл или директория. ("dir" or "file").
        download_link (str): Ссылка для скачивания ресурса.
        MIME_type (str): MIME тип файла (например: image/png)
    """
    def __init__(self, name: str, path: str, size: Optional[int], download_link: str, type: str, MIME_type: str):
            """
            Функция для инициализация объекта File.
            
            """
            self.name = name
            self.path = path
            self.download_link = download_link
            self.size = size
            self.type = type
            self.MIME_type = MIME_type
    
    """
    Функция для репрезентации объекта File.
    Данная функция была реализована с целью подтверждения 
    правильной инициализации объекта.
    """
    def __repr__(self):
        return f"File(name={self.name!r}, path={self.path!r}, download_link={self.download_link!r}, size={self.size!r}, type={self.type!r}, MIME_type={self.MIME_type!r})"
    
    



        
