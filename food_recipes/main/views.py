from django.shortcuts import render

from django.http import HttpResponse

from .models import Product


def index(request):
    if request.method == 'POST':
        colors = request.POST.get("colors", False)
        print(colors)
        
        title = request.POST.get("title", False)
        print(title)

    lst = ['1', '2', '3']
   
    products = [
        Product('Water efrege etbgetb', 'cake_plum_cake_streusel.jpg', '3'),
        Product('Water efrege etbgetb', 'cake_tart_pastries_small_0.jpg', '4'),
        Product('Water efrege etbgetb', 'cooking_fusion_cuisine_.jpg', '5'),
    ]
    
    context = {'title': 'Главная страница', 
            'lst': lst,
            'products': products,
            'menu': get_menu()
            }
    return render(request, "main/index.html", context)


def get_menu():
    title = ('Главная', 'Галерея', ) # 'Мой профиль', 'Регистрация', 'Вход в аккаунт'
    logo = ('fa fa-regular fa-flag', 'fa fa-regular fa-calendar', ) # 'fa fa-regular fa-address-book', 'fa fa-regular fa-user-circle-o', 'fa fa-regular fa-arrow-circle-right'
    menu = zip(title, logo)
    return menu


def sidebar(request):
    return render(request, "main/sidebar.html", {'nums': range(0, 6), 'menu': get_menu()})


def show_about(request):
    return HttpResponse("<h1>О нас</h1>")


def contacts(request):
    return HttpResponse("<h1>Контакты</h1>")


def foodlist(request):

    products = [
        # Product('Water efrege etbgetb', 'jambalaya_.jpg', '1'),
        Product('Water efrege etbgetb', 'cake_baking_.jpg', '2'),
        Product('Water efrege etbgetb', 'cake_plum_cake_streusel.jpg', '3'),
        Product('Water efrege etbgetb', 'cake_tart_pastries_small_0.jpg', '4'),
        Product('Water efrege etbgetb', 'cooking_fusion_cuisine_.jpg', '5'),
        # Product('Water efrege etbgetb', 'pizza_food_cooking_broccoli.jpg', '6'),
        # Product('Water efrege etbgetb', 'pizza_food_cooking_broccoli.jpg', '7'),
        Product('Water efrege etbgetb', 'salad_mixed_salad_cucumber.jpg', '8'),
        Product('Water efrege etbgetb', 'pizza_food_cooking_broccoli.jpg', '9'),
    ]

    context = {'title': 'Галерея', 
               'products': products,
               }
    return render(request, "main/foodlist.html", context)
