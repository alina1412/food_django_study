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
    water = Product('Water efrege etbgetb', 'product06.jpg', '21')
    products = [water, water, water]
    
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
    water = Product('Water efrege etbgetb', 'product06.jpg', '21')
    products = [water, water, water]
    context = {'title': 'Галерея', 
               'products': products,
               }
    return render(request, "main/foodlist.html", context)
