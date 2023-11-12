from django.db import models



class Product:
    def __init__(self, title, img, dop):
        self.title = title
        self.img = img
        self.dop = dop