from django import forms 

class LinkForm(forms.Form):
    link = forms.CharField(max_length=255)

class FileFilterForm(forms.Form):
    FILE_TYPE_CHOICES = [
        ('all', 'Все файлы'),
        ('text', 'Текстовые файлы'),
        ('image', 'Фотографии'),
        ('video', 'Видео-Файлы'),
        ('application', 'Аппликации'),
        ('font', 'Шрифты'),
        ('audio', 'Аудио-Файлы')
    ]
    file_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, required=False, initial='all')
   

    

