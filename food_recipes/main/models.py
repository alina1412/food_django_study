from django.db import models


class Product:
    def __init__(self, id, title, img, detail):
        self.id = id
        self.title = title
        self.img = img
        self.detail = detail


class Recipe:
    def __init__(self, title, author, description, date, category, files):
        self.title = title
        self.author = author
        self.description = description
        self.date = date
        self.category = category
        self.files = files


description = """
    Музыка: Людвиг ван Бетховен, Александр Вертинский, Пьер Дегейтер, Павел Зубаков, Василий Липатов, 
    Карл Орф, Григорий Пономаренко, Сергей Рахманинов, Георгий Свиридов, Камилл Сен-Санс, Александр Флярковский, 
    Арам Хачатурян, Петр Чайковский, Альфред Шнитке, Фридерик Шопен, Винсент Юманс, 
    русские народные песни и танцы Стихи: Сергей Есенин, Александр Пушкин, Сергей Бехтеев, Александр Блок, Зинаида Гиппиус 
"""
