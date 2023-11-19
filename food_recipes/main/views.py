import datetime
from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Product, Recipe, description


def index(request):
    if request.method == "POST":
        colors = request.POST.get("colors", False)
        print(colors)

        title = request.POST.get("title", False)
        print(title)

    products = [
        Product('3', "Water efrege etbgetb", "cake_plum_cake_streusel.jpg", "3"),
        Product('4', "Water efrege etbgetb", "cake_tart_pastries_small_0.jpg", "4"),
        Product('5', "Water efrege etbgetb", "cooking_fusion_cuisine_.jpg", "5"),
    ]

    context = {
        "title": "Главная страница",
        "products": products,
    }
    return render(request, "main/index.html", context)


def sidebar(request):
    return render(
        request, "main/sidebar.html"
    )


def profile(request):
    user = User.objects.get(id=request.user.id)
    ava = ""
    context = {
        "title": "Профиль",
        "profile": user,
        "ava": ava,
    }
    return render(request, "main/profile.html", context)


def contacts(request):
    context = {
        "title": "Контакты",
    }
    return render(request, "main/contacts.html", context)


def login(request):
    context = {
        "title": "Войти",
        "btn_text": "Войти",
    }
    return render(request, "main/login.html", context)


def register(request):
    context = {
        "title": "Регистрация",
        "btn_text": "Регистрация",
    }
    return render(request, "main/login.html", context)



def foodlist(request, cat_id):
    products = [
        # Product('Water efrege etbgetb', 'jambalaya_.jpg', '1'),
        Product('2', "Water efrege etbgetb", "cake_baking_.jpg", description),
        Product('3', "Water efrege etbgetb", "cake_plum_cake_streusel.jpg", description),
        Product('4', "Water efrege etbgetb", "cake_tart_pastries_small_0.jpg", description),
        Product('5', "Water efrege etbgetb", "cooking_fusion_cuisine_.jpg", description),
        # Product('Water efrege etbgetb', 'pizza_food_cooking_broccoli.jpg', '6'),
        # Product('Water efrege etbgetb', 'pizza_food_cooking_broccoli.jpg', '7'),
        Product('8', "Water efrege etbgetb", "salad_mixed_salad_cucumber.jpg", description),
        Product('9', "Water efrege etbgetb", "pizza_food_cooking_broccoli.jpg", description),
    ]

    context = {
        "title": f"Категория {cat_id}",
        "products": products,
    }
    return render(request, "main/foodlist.html", context)


def gallery(request):
    products = [
        Product('2', "Water efrege etbgetb", "cake_baking_.jpg", "2"),
        Product('3', "Water efrege etbgetb", "cake_plum_cake_streusel.jpg", "3"),
        Product('4', "Water efrege etbgetb", "cake_tart_pastries_small_0.jpg", "4"),
        Product('5', "Water efrege etbgetb", "cooking_fusion_cuisine_.jpg", "5"),
        Product('8', "Water efrege etbgetb", "salad_mixed_salad_cucumber.jpg", "8"),
        Product('9', "Water efrege etbgetb", "pizza_food_cooking_broccoli.jpg", "9"),
    ]

    context = {
        "title": "Галерея",
        "products": products,
    }
    return render(request, "main/gallery.html", context)


def details(request, id):
    rec1 = Recipe(
        '1',
        f"Мой салатик {id}",
        "Мария З.",
        description,
        datetime.datetime.now(),
        "Салаты",
        ["salad_mixed_salad_cucumber.jpg", "salad_mixed_salad_cucumber.jpg"],
        "salad_mixed_salad_cucumber.jpg",
    )

    context = {
        "title": "",
        "recipe": rec1,
    }
    return render(request, "main/recipe.html", context)


def not_found_view(request, exception):
    return render(request, "main/404.html")