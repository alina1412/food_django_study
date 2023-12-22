from django.db import models
# from django.utils.html import escape
from django.utils.html import mark_safe

from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    TextField,
    DateTimeField,
    ManyToManyField,
)
from django.contrib.auth.models import User

import pathlib

from food_recipes.settings import MEDIA_URL

FOLDER = pathlib.Path(__file__).parent.resolve()


class Product:
    def __init__(self, id, title, img, detail):
        self.id = id
        self.title = title
        self.img = img
        self.detail = detail


# class Recipe:
#     def __init__(self, id_, title, author, description, date, category, files, img):
#         self.id = id_
#         self.title = title
#         self.author = author
#         self.description = description
#         self.date = date
#         self.category = category
#         self.files = files
#         self.img = img


class Category(Model):
    food_type = TextField("Название", max_length=100)

    def __str__(self):
        return self.food_type

    class Meta:
        verbose_name = "Категория (Category)"
        verbose_name_plural = "Категории"


class Recipe(Model):  # title, author, description, date, category, files, img
    title = TextField("Название", max_length=250)
    author = ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )  # удалит рецепт при удалении юзера
    description = TextField("Описание")
    date = DateTimeField("Дата публикации", auto_now=True, auto_created=True)
    category = ManyToManyField(to=Category, blank=True, verbose_name="Категория")
    votes = models.IntegerField('Голоса', blank=True, null=True, auto_created=True, default=0)

    def get_fields(self):
        return [
            (field.name, getattr(self, field.name)) for field in Recipe._meta.fields
        ]

    def __str__(self):
        return self.title
    class Meta:
        # ordering = ['itle','status']
        verbose_name= 'Рецепт (Recipe)'
        verbose_name_plural='Рецепты'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.rec_id, filename)


class File(Model):
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE, related_name="images")
    # filename =  CharField("filename", max_length=40)
    file = models.ImageField(upload_to="import", blank=True, null=True)
    
    def image_tag(self):
        return mark_safe(f'<img height=30px src="{MEDIA_URL}%s" />' % (self.file))
    
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return str(self.recipe.id)
    class Meta:
        # ordering = ['itle','status']
        verbose_name= 'Файл (File)'
        verbose_name_plural='Файлы'


description = """
    Музыка: Людвиг ван Бетховен, Александр Вертинский, Пьер Дегейтер, Павел Зубаков, Василий Липатов, 
    Карл Орф, Григорий Пономаренко, Сергей Рахманинов, Георгий Свиридов, Камилл Сен-Санс, Александр Флярковский, 
    Арам Хачатурян, Петр Чайковский, Альфред Шнитке, Фридерик Шопен, Винсент Юманс, 
    русские народные песни и танцы Стихи: Сергей Есенин, Александр Пушкин, Сергей Бехтеев, Александр Блок, Зинаида Гиппиус 
"""
