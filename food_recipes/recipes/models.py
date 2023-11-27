from django.db import models
from django.db.models import Model, ForeignKey, CharField, TextField, DateTimeField
from django.contrib.auth.models import User



class Category2(Model):
    food_type = TextField("Название", max_length=100)


class Recipe2(Model): # title, author, description, date, category, files, img
    title = TextField("Название", max_length=250)
    author = ForeignKey(User, on_delete=models.CASCADE)  # удалит рецепт при удалении юзера
    description = TextField("Описание")
    date = DateTimeField('Дата публикации', auto_now=True, auto_created=True)
    category = ForeignKey(Category2, on_delete=models.SET_NULL, null=True, blank=True)
    # files = TextField("Картинки", null=True, blank=True)

    def get_fields(self):
        return [(field.name, getattr(self,field.name)) for field in Recipe2._meta.fields]


# class File2(Model):
#     rec_id = ForeignKey(Recipe2, on_delete=models.CASCADE)
#     filename =  CharField("filename", max_length=40)

description = '''
Музыка: Людвиг ван Бетховен, Александр Вертинский, Пьер Дегейтер, Павел Зубаков, Василий Липатов, Карл Орф, Григорий Пономаренко, Сергей Рахманинов, Георгий Свиридов, Камилл Сен-Санс, Александр Флярковский, Арам Хачатурян, Петр Чайковский, Альфред Шнитке, Фридерик Шопен, Винсент Юманс, русские народные песни и танцы Стихи: Сергей Есенин, Александр Пушкин, Сергей Бехтеев, Александр Блок, Зинаида Гиппиус 

'''