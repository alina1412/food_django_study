from django.db import models



class Product:
    def __init__(self, title, img, detail):
        self.title = title
        self.img = img
        self.detail = detail
