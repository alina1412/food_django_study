import pathlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    TextField,
)
from django.utils.html import mark_safe

FOLDER = pathlib.Path(__file__).parent.resolve()


class Product:
    def __init__(self, id, title, img, detail):
        self.id = id
        self.title = title
        self.img = img
        self.detail = detail


class Category(Model):
    food_type = TextField("Название", max_length=100)

    def __str__(self):
        return self.food_type

    class Meta:
        verbose_name = "Категория (Category)"
        verbose_name_plural = "Категории"


class Recipe(Model):
    title = TextField("Название", max_length=250)
    author = ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )  # удалит рецепт при удалении юзера
    description = TextField("Описание")
    date = DateTimeField("Дата публикации", auto_now=True, auto_created=True)
    category = ManyToManyField(
        to=Category, blank=True, verbose_name="Категория"
    )
    votes = models.IntegerField(
        "Голоса", blank=True, null=True, auto_created=True, default=0
    )

    def get_fields(self):
        return [
            (field.name, getattr(self, field.name))
            for field in Recipe._meta.fields
        ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепт (Recipe)"
        verbose_name_plural = "Рецепты"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.rec_id, filename)


class File(Model):
    recipe = ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="images"
    )
    # filename =  CharField("filename", max_length=40)
    file = models.ImageField(upload_to="import", blank=True, null=True)

    def image_tag(self):
        return mark_safe('<img height=30px src="{}" />'.format(self.file.url))

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def __str__(self):
        return str(self.recipe.id)

    class Meta:
        verbose_name = "Файл (File)"
        verbose_name_plural = "Файлы"
