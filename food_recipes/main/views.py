import datetime
from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max

from .models import Product, Recipe, description, File, Category


def index(request):
    if request.method == "POST":
        colors = request.POST.get("colors", False)
        print(colors)

        title = request.POST.get("title", False)
        print(title)

    # cnt = User.objects.annotate(Count('recipe', distinct=True)).aggregate(Avg('recipe__count'))
    # cnt = User.objects.annotate(Count('recipe', distinct=True)).order_by('-recipe__count').values('username').first()
    # print(cnt)
    # search = User.objects.annotate(Count('recipe', distinct=True))
    # cnt = search.aggregate(Max('recipe__count'))

    # max_article_count_user2 = search.filter(recipe__count__exact=cnt['recipe__count__max'])
    # print(max_article_count_user2)

    """recepies = User.objects.raw('''select 1 as id, main_recipe.title from auth_user 
                                left join main_recipe on main_recipe.author_id = auth_user.id
                                where auth_user.id = %s''', params='1')
    print([x.title for x in recepies])"""

    recipes = Recipe.objects.all()
    recs_id_list = [int(rec.id) for rec in recipes]
    print(recs_id_list)
    recs = File.objects.filter(rec_id__in=recs_id_list).values("id", "file")
    files = {int(file["id"]): file["file"] for file in recs}

    context = {
        "title": "Главная страница",
        # "lst": lst,
        "products": recipes,
        "menu": get_menu(),
        "files": files,
    }
    return render(request, "main/index.html", context)


def get_menu():
    title = ("Главная", "Галерея")  # 'Мой профиль', 'Регистрация', 'Вход в аккаунт'
    logo = (
        "fa fa-regular fa-flag",
        "fa fa-regular fa-calendar",
    )  # 'fa fa-regular fa-address-book', 'fa fa-regular fa-user-circle-o', 'fa fa-regular fa-arrow-circle-right'
    menu = zip(title, logo)
    return menu


def sidebar(request):
    return render(
        request, "main/sidebar.html", {"nums": range(0, 6), "menu": get_menu()}
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


def get_login_dict():
    return {
        "name": {"title": "Имя", "type": "text"},
        "email": {"title": "email", "type": "text"},
        "password1": {"title": "Пароль", "type": "password"},
        "password2": {"title": "Подтвердите пароль", "type": "password"},
    }


def login(request):
    log_dict = get_login_dict()
    # log_dict['type'] = 'login'
    context = {
        "title": "Войти",
        "btn_text": "Войти",
        "login": log_dict,
    }
    return render(request, "main/login.html", context)


def register(request):
    # if request.POST:
    #     form = GeeksForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES["geeks_field"])
    log_dict = get_login_dict()
    # log_dict['type'] = 'register'
    context = {
        "title": "Регистрация",
        "btn_text": "Регистрация",
        "login": log_dict,
    }
    return render(request, "main/login.html", context)


def foodlist(request, cat_id):
    """по категориям"""
    # cat_id = "1"
    print("categ", cat_id)
    recipes = Recipe.objects.filter(category__id=cat_id).all()
    # print([(rec.id, rec.description) for rec in recipes])
    recs_id_list = [rec.id for rec in recipes]
    print(recs_id_list)
    recs = File.objects.filter(rec_id__in=recs_id_list).values("rec_id", "file")
    files = {int(file["rec_id"]): file["file"] for file in recs}
    print('files',files)
    context = {
        "title": "Категория",
        "products": recipes,
        "files": files,
    }
    return render(request, "main/foodlist.html", context)


def gallery(request):

    recipes = Recipe.objects.all()
    recs_id_list = [int(rec.id) for rec in recipes]
    print(recs_id_list)
    recs = File.objects.filter(rec_id__in=recs_id_list).values("id", "file")
    files = {int(file["id"]): file["file"] for file in recs}

    context = {
        "title": "Галерея",
        "products": recipes,
        "files": files,
    }
    return render(request, "main/gallery.html", context)


def details(request, id):
    # Recipe.objects.all().first()
    # files
    # rec1 = Recipe.objects.filter(id='1')
    """print(request.user.id)
    author = User.objects.get(id=request.user.id)
    print(author, 'author')"""
    # new_ = Recipe(author=author, title='gbrb', description='ftrbg')
    # new_.save()
    rec1 = Recipe.objects.filter(id=id).first()

    files = File.objects.filter(rec_id=rec1)
    print("files", [file for file in files])

    context = {
        "title": "",
        "recipe": rec1,
        "files": files,
    }
    return render(request, "main/recipe.html", context)


def not_found_view(request, exception):
    return render(request, "main/404.html")


def get_files_of_recipe(rec_id):
    rec1 = Recipe.objects.filter(id=id).first()
    return File.objects.filter(rec_id=rec1)


def save_new_file(request):
    recipe_id = request.POST.get("recipe_id")
    filename = request.POST.get("filename")

    if not filename and not recipe_id:
        ...
    else:
        recipe_obj = Recipe.objects.get(id=recipe_id)
        new_file = File(filename=filename, rec_id=recipe_obj)
        new_file.save()


def save_new_recipe(request):
    title = request.POST.get("title")
    user_id = request.POST.get("request.user.id")
    description = request.POST.get("description")
    category_id = request.POST.get("category_id")
    filename = request.POST.get("filename")
    # title, author, description, date, category, files

    if not 1 == 0:
        ...
    else:
        author = User.objects.get(id=user_id)
        category = Category.objects.get(id=category_id)
        new_recipe = Recipe(
            title=title,
            author=author,
            description=description,
            date=datetime.datetime.now(),
            category=category,
        )
        new_recipe.save()
        return new_recipe["id"]


"""    rec1 = Recipe(
        title="Мой салатик",
        author=User.objects.get(id=request.user.id),
        description=description,
        date=datetime.datetime.now(),
        # category=category.set()
    )
    rec1.save()
    rec1.category.add('1')
    rec1.save()"""
