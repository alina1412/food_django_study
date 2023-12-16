import datetime
from typing import Any
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Max
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.conf import settings
from django.db.models.query_utils import Q

from .models import Product, Recipe, description, File, Category
from .forms import *
from users.models import Account


def index(request):
    context = {
        "title": "Главная страница",
        "products": tuple(),
        "files": tuple(),
        "search_res": False
    }
    if request.method == "POST":
        title = request.POST.get("title", False)
        my_rec = request.POST.get("my_recipes", False)
        if title:
            title = title.strip()
            recipes, files = get_recipes_and_first_file(with_filter={'title': title})
        
        elif my_rec:
            if request.user.id:
                recipes, files = get_recipes_and_first_file(with_filter={'author': request.user.id})

        else:
            recipes, files = get_recipes_and_first_file()
        
        context["products"] = recipes
        context['files'] = files
        context["search_res"] = title
        context["title"] = "Главная страница" if not my_rec  else "Мои рецепты"
      
        return render(request, "main/index.html", context)
    winners = Recipe.objects.annotate(Count('stars', distinct=True))

    recipes, files = get_recipes_and_first_file()

    context["products"] = recipes
    context['files'] = files

    return render(request, "main/index.html", context)


def sidebar(request):
    return render(
        request, "main/sidebar.html"
    )


def users_top(request):
    '''топ юзеров по количеству рецептов'''
    users_top = User.objects.annotate(Count('recipe', distinct=True)).select_related('account').order_by('-recipe__count')
    # .values('account__nickname, recipe__count')
    # cnt.first().recipe__count
    context = {'users_top': users_top}
    return render(request, "main/users_top.html", context)


def contacts(request):
    context = {
        "title": "Контакты",
    }
    return render(request, "main/contacts.html", context)



def foodlist(request, cat_id):
    """по категориям"""
    recipes = Recipe.objects.filter(category__id=cat_id).all()
    category = Category.objects.filter(id=cat_id).first()
    # print([(rec.id, rec.description) for rec in recipes])
    recs_id_list = [rec.id for rec in recipes]
    print(recs_id_list)
    recs = File.objects.filter(recipe__in=recs_id_list).values("recipe", "file")
    files = {int(file["recipe"]): file["file"] for file in recs}
    print('files',files)
    context = {
        "title": "Категория",
        'food_type': category.food_type,
        "products": recipes,
        "files": files,
    }
    return render(request, "main/foodlist.html", context)


def gallery(request):
    recipes, files = get_recipes_and_first_file()

    context = {
        "title": "Галерея",
        "products": recipes,
        "files": files,
    }
    return render(request, "main/gallery.html", context)


def details(request, id):
    rec1 = Recipe.objects.filter(id=id).select_related('author').first()
    account = Account.objects.get(user=rec1.author)
    # .values_list('title', 'author', 'date', 'id', 'description')
    files = File.objects.filter(recipe=id)
    print("details files", files)

    context = {
        "title": "",
        "recipe": rec1,
        "files": files,
        'account': account
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


# def save_new_recipe(request):
#     title = request.POST.get("title")
#     user_id = request.POST.get("request.user.id")
#     description = request.POST.get("description")
#     category_id = request.POST.get("category_id")
#     filename = request.POST.get("filename")
#     # title, author, description, date, category, files

#     if not 1 == 0:
#         ...
#     else:
#         author = User.objects.get(id=user_id)
#         category = Category.objects.get(id=category_id)
#         new_recipe = Recipe(
#             title=title,
#             author=author,
#             description=description,
#             date=datetime.datetime.now(),
#             category=category,
#         )
#         new_recipe.save()
#         return new_recipe["id"]


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


def get_recipes_and_first_file(with_filter=False):
    if not with_filter:
        recipes = Recipe.objects.select_related("author").prefetch_related("images").all()
    elif with_filter.get('author'):
        recipes = Recipe.objects.filter(author=with_filter.get('author')).select_related("author").prefetch_related("images").all()
    else:
        title = with_filter.get('title')
        recipes = Recipe.objects.select_related("author").prefetch_related("images").filter(Q(title__icontains=title)|Q(description__icontains=title))
    print([(r.id, r.images.first()) for r in recipes])
    files =  {int(file.id): [file.images.first().file if file.images.first() else None]  for file in recipes}
    print('gallery files', files)
    return recipes, files



@login_required(login_url=settings.LOGIN_URL)
def add_recipe(request):
    if request.method == 'POST':
        if not request.user.id:
            return HttpResponse('вы не залогинены')
        form = RecipeAddForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            new_recipe = form.save(commit=False)
            new_recipe.author = current_user
            new_recipe.save()
            form.save_m2m()
            for img in request.FILES.getlist('file'):
                File.objects.create(recipe=new_recipe, file=img)
           
            return redirect('/')
    else:
        form = RecipeAddForm()
    return render(request,'main/upload.html', {'form':form })
