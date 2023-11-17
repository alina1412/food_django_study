from django.db import models
from django.db.models import Model, ForeignKey, CharField, TextField, DateTimeField
from django.contrib.auth.models import User


class Category(Model):
    food_type = TextField("Название", max_length=100)


class Recipe(Model):
    title = TextField("Название", max_length=250)
    author = ForeignKey(User, on_delete=models.CASCADE)  # удалит рецепт при удалении юзера
    description = TextField("Описание")
    date = DateTimeField('Дата публикации', auto_now=True, auto_created=True)
    category = ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    files = TextField("Картинки", null=True, blank=True)

    def get_fields(self):
        return [(field.name, getattr(self,field.name)) for field in Recipe._meta.fields]


class Product:
    def __init__(self, title, img, detail):
        self.title = title
        self.img = img
        self.detail = detail

description = '''
Музыка: Людвиг ван Бетховен, Александр Вертинский, Пьер Дегейтер, Павел Зубаков, Василий Липатов, Карл Орф, Григорий Пономаренко, Сергей Рахманинов, Георгий Свиридов, Камилл Сен-Санс, Александр Флярковский, Арам Хачатурян, Петр Чайковский, Альфред Шнитке, Фридерик Шопен, Винсент Юманс, русские народные песни и танцы Стихи: Сергей Есенин, Александр Пушкин, Сергей Бехтеев, Александр Блок, Зинаида Гиппиус 

'''