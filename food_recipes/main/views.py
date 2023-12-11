import datetime
from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max
from django.views.generic import DetailView, DeleteView, UpdateView
from django.contrib import messages
from django.db.models.query_utils import Q

from .models import Product, Recipe, description, File, Category
from .forms import *

def index(request):
    if request.method == "POST":
        title = request.POST.get("title", False)
        if title:
            title = title.strip()
        print(title)
        
        recipes, files = get_recipes_and_first_file(with_filter=title)

        context = {
            "title": "Главная страница",
            "products": recipes,
            "menu": get_menu(),
            "files": files,
            "search_res": title
        }
        return render(request, "main/index.html", context)
    winners = Recipe.objects.annotate(Count('stars', distinct=True))
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
        "search_res": False
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


# def profile(request):
#     user = User.objects.get(id=request.user.id)
#     ava = ""
#     form = ProfileForm()
#     context = {
#         "title": "Профиль",
#         "profile": user,
#         "ava": ava,
#         'form': form
#     }
#     return render(request, "main/profile.html", context)
def users_top(request):
    '''топ юзеров по количеству рецептов'''
    users_top = User.objects.annotate(Count('recipe', distinct=True))
    # cnt.first().recipe__count
    context = {'users_top': users_top}
    return render(request, "main/users_top.html", context)


def contacts(request):
    context = {
        "title": "Контакты",
    }
    return render(request, "main/contacts.html", context)


def get_login_dict():
    return {
        "username": {"title": "Имя", "type": "text"},
        # "email": {"title": "email", "type": "text"},
        "password1": {"title": "Пароль", "type": "password"},
        "password2": {"title": "Подтвердите пароль", "type": "password"},
    }





# def registerView(request):
#     from django.contrib.auth import authenticate
#     from django.contrib import messages
#     from django.contrib.messages import get_messages
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             # authenticate(username=username,password=password)
#             login(request, user)
#             return redirect('main:main')
#         else:
#             print(form.errors)
           
#             context = {"title": "Регистрация", "btn_text": "Регистрация",  'form': form, 'messages':get_messages(request) }
#             return render(request, "main/login.html", context)
#     else:
#         if request.user.is_authenticated:
#             messages.add_message(request, messages.SUCCESS, 'Вы уже залогинились на сайте')
#             # messages.success(request, 'Вы уже залогинились на сайте', extra_tags='success')

#     context = {"title": "Регистрация", "btn_text": "Регистрация", 'form':RegisterForm(), 'messages':get_messages(request) }
#     return render(request, "main/login.html", context)


# from django.shortcuts import render, redirect 
# from django.contrib import messages
# from django.contrib.auth.views import LoginView

 
# class CustomLoginView(LoginView):
#     form_class = LoginForm
#     redirect_authenticated_user = True
#     initial = {'key': 'value'}
#     template_name = 'main/login.html'
#     context = {"title": "Войти", "btn_text": "Войти"}
  
#     def get_success_url(self):
#         return reverse_lazy('main:main') 
    
#     def form_invalid(self, form):
#         messages.error(self.request,'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))
#     # def get(self, request, *args, **kwargs):
#     #     if request.user.is_authenticated:
#     #         messages.success(request, 'Вы уже залогинились на сайте.')
#     #         return redirect('main:main')
#     #     form = self.form_class(initial=self.initial)
#     #     self.context['form'] = form
#     #     return render(request, self.template_name, self.context)
        
#     # def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')        
#             user = authenticate(username=username,password=password)
#             login(request, user)
#             return redirect('main:main')
        
#         self.context['form'] = form #'messages':get_messages(request)
#         return render(request, self.template_name, self.context )



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


def get_recipes_and_first_file(with_filter=False):
    if not with_filter:
        recipes = Recipe.objects.select_related("author").prefetch_related("images").all()
    else:
        title = with_filter
        recipes = Recipe.objects.select_related("author").prefetch_related("images").filter(Q(title__icontains=title)|Q(description__icontains=title))
    print([(r.id, r.images.first()) for r in recipes])
    files =  {int(file.id): [file.images.first().file if file.images.first() else None]  for file in recipes}
    print('gallery files', files)
    return recipes, files