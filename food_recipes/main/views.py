from django.shortcuts import render

from django.http import HttpResponse

# from .models import News, Product


def index(request):
    if request.method == 'POST':
        colors = request.POST.get("colors", False)
        print(colors)
        
        title = request.POST.get("title", False)
        print(title)

    lst = ['1', '2', '3']

    context = {'title': 'Главная страница', 
            'lst': lst,
            'menu': get_menu()
            }
    return render(request, "main/index.html", context)


def get_menu():
    title = ('Домой', 'Новости', 'Мой профиль', 'Регистрация', 'Вход в аккаунт')
    logo = ('fa-regular fa-flag', 'fa-regular fa-calendar', 'fa-regular fa-address-book', 'fa-regular fa-circle-user', 'fa-regular fa-circle-right')
    menu = zip(title, logo)
    return menu


def sidebar(request):
    return render(request, "main/sidebar.html", {'nums': range(0, 6), 'menu': get_menu()})


def show_about(request):
    return HttpResponse("<h1>О нас</h1>")


def contacts(request):
    return HttpResponse("<h1>Контакты</h1>")


def foodlist(request):
    context = {}
    return render(request, "main/foodlist.html", context)
