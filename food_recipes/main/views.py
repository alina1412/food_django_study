import datetime
from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max
from django.views.generic import DetailView, DeleteView, UpdateView

from .models import Product, Recipe, description, File, Category
from .forms import *

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

    # recipes = Recipe.objects.all()
    # recs_id_list = [int(rec.id) for rec in recipes]
    # print(recs_id_list)
    # recs = File.objects.filter(recipe__in=recs_id_list).values("id", "file")
    # files = {int(file["id"]): file["file"] for file in recs}
    # sql = '''SELECT recipe_id as id, main_file.file as img, main_recipe.title, main_recipe.stars 
    #         FROM main_recipe
    #         inner join main_file on main_file.recipe_id = main_recipe.id
    #         WHERE main_recipe.id IN (SELECT id FROM main_recipe)
    #         group by  main_recipe.id
    #         ;'''
    # recipes = Recipe.objects.raw(sql)
    # print([r for r in recipes])
    # files =  {int(file.id): [file.img]  for file in recipes}

    # recipes, files = get_recipes_and_files()
    recipes, files = get_recipes_and_first_file()
    # print([r.stars for r in recipes])

    context = {
        "title": "Главная страница",
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
    form = ProfileForm()
    context = {
        "title": "Профиль",
        "profile": user,
        "ava": ava,
        'form': form
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
    recs = File.objects.filter(recipe__in=recs_id_list).values("recipe", "file")
    files = {int(file["recipe"]): file["file"] for file in recs}
    print('files',files)
    context = {
        "title": "Категория",
        'cat_id': cat_id,
        "products": recipes,
        "files": files,
    }
    return render(request, "main/foodlist.html", context)


def gallery(request):

    # recipes = Recipe.objects.all()
    '''SELECT rec_id FROM "main_recipe"'''
    
    """sql = '''SELECT recipe_id as id, main_file.file as img, main_recipe.title, main_recipe.stars 
            FROM main_recipe
            left join main_file on main_file.recipe_id = main_recipe.id
            WHERE main_file.recipe_id IN (SELECT id FROM main_recipe)
            group by recipe_id
            ;'''
    recipes = Recipe.objects.raw(sql)
    print([(f.id, f.img) for f in recipes])"""
    recipes, files = get_recipes_and_first_file()

    # recs_id_list = [int(rec.id) for rec in recipes]
    # print(recs_id_list)
    # recs = File.objects.filter(rec_id__in=recs_id_list).values("id", "file")
    # files = {int(file["id"]): file["file"] for file in recipes}
    # return render(request, "main/index.html")
    context = {
        "title": "Галерея",
        "products": recipes,
        "files": files,
    }
    return render(request, "main/gallery.html", context)


def details(request, id):
    rec1 = Recipe.objects.filter(id=id).select_related('author').first()
    # .values_list('title', 'author', 'date', 'id', 'description')
    # files = rec1.file_set.all()
    files = File.objects.filter(recipe=id)
    """SELECT * FROM "main_file" 
    INNER JOIN "main_recipe" ON ("main_file"."recipe_id" = "main_recipe"."id") 
    INNER JOIN "auth_user" ON ("main_recipe"."author_id" = "auth_user"."id") 
    WHERE "main_file"."recipe_id" = '1'"""

    # sql = '''SELECT * --rec_id_id as id, main_recipe.title, main_recipe.stars 
    #         FROM main_recipe
    #         left join main_file on main_file.rec_id_id = main_recipe.id
    #         WHERE main_recipe.id = 1
           
    #         ;'''
    # rec1 = Recipe.objects.raw(sql) # , params=id
    print("details files", files)
    # print(rec1)

    context = {
        "title": "",
        "recipe": rec1,
        "files": files,
    }
    return render(request, "main/recipe.html", context)


def not_found_view(request, exception):
    return render(request, "main/404.html")


def get_files_of_recipe(rec_id):
    rec1 = Recipe.objects.filter(id=rec_id).first()
    return File.objects.filter(recipe=rec1)


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

"""print(request.user.id)
author = User.objects.get(id=request.user.id)
print(author, 'author')"""

def get_recipes_and_files():
    recipes = Recipe.objects.select_related("author").prefetch_related("images").all()
    print([(r.id, r.images.all()) for r in recipes])
    files =  {int(file.id): [ff.file for ff in file.images.all()]  for file in recipes}
    # print('gallery files', [list([ff.file for ff in v]) for f,  v in files.items()])
    print('gallery files', files)
    return recipes, files


def get_recipes_and_first_file():
    recipes = Recipe.objects.select_related("author").prefetch_related("images").all()
    print([(r.id, r.images.first()) for r in recipes])
    files =  {int(file.id): [file.images.first().file if file.images.first() else None]  for file in recipes}
    print('gallery files', files)
    return recipes, files