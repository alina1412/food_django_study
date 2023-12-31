import datetime
from typing import Any
from django.db import models
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.messages import get_messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Max
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.db.models.query_utils import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Recipe, File, Category
from .forms import *
from users.models import Account, VotesConnection


def index(request):
    context = {
        "title": "Главная страница",
        "recipes": tuple(),
        "files": tuple(),
        "search_res": False,
        'total': 0,
        "liked": find_what_liked(request)
    }
    page_number = request.GET.get('page')

    if request.method == "POST":
        page_number = 0
        title = request.POST.get("title", False)
        my_rec = request.POST.get("my_recipes", False)
        if title:
            title = title.strip()
            recipes_page, files, total = get_recipes_and_first_file(with_filter={'title': title}, page_number=page_number)
        
        elif my_rec:
            if request.user.id:
                recipes_page, files, total = get_recipes_and_first_file(with_filter={'author': request.user.id}, page_number=page_number)

        else:
            recipes_page, files, total = get_recipes_and_first_file()
        
        context["recipes"] = recipes_page
        context['files'] = files
        context["search_res"] = title
        context["title"] = "Главная страница" if not my_rec  else "Мои рецепты"
        context['total'] = total
      
        return render(request, "main/index.html", context)
    winners = Recipe.objects.annotate(Count('votes', distinct=True))

    recipes_page, files, total = get_recipes_and_first_file(False, page_number)

    context["recipes"] = recipes_page
    context['files'] = files
    context['total'] = total
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

    total = len(recipes)
    page_number = request.GET.get('page')

    page_paginator = Paginator(recipes, per_page=4)
    recipes_page = page_paginator.get_page(page_number)

    # print([(rec.id, rec.description) for rec in recipes])
    recs_id_list = [rec.id for rec in recipes_page]
    print(recs_id_list)
    recs = File.objects.filter(recipe__in=recs_id_list).values("recipe", "file")
    files = {int(file["recipe"]): (file["file"],) for file in recs}
    # print('files',files)
    liked_recipes_dict = find_what_liked(request)

    context = {
        "title": "Категория",
        'food_type': category.food_type if category else None,
        "recipes": recipes_page,
        "files": files,
        "liked": liked_recipes_dict,
        'total': total
    }
    return render(request, "main/foodlist.html", context)


def gallery(request):
    page_number = request.GET.get('page')

    recipes_page, files, total = get_recipes_and_first_file(False, page_number)
    liked_recipes_dict = find_what_liked(request)

    context = {
        "title": "Галерея",
        "recipes": recipes_page,
        "files": files,
        "liked": liked_recipes_dict,
        'total': total
    }
    return render(request, "main/gallery.html", context)


def find_what_liked(request):
    if not request.user or not request.user.id:
        ...# user='anonymous'
        return {}
    else:
        user = Account.objects.get(user=request.user.id)
        
        liked_recipes_dict = {}
        # VotesConnection(recipe=rec1, user=user
        for rec in user.likes_recipes.all():
            liked_recipes_dict[rec.id] = 1
        return liked_recipes_dict


def stared(request, id):
    try:
        id = int(id)
    except Exception:
        return not_found_view(request=request, exception='')
    rec1 = Recipe.objects.filter(id=id).first()
    if not rec1:
        print('-----not found recipe-', id)
        return not_found_view(request=request, exception='')
    if not request.user or not request.user.id:
        ...# user='anonymous'
        return HttpResponse('fail')
    else:
        user = Account.objects.get(user=request.user.id)
        liked = VotesConnection.objects.filter(
                recipe=rec1, user=user).first()
        if not liked:
            VotesConnection(recipe=rec1, user=user).save()

            rec1.votes += 1
            rec1.save()
        else:
            return HttpResponse('voted')
    return HttpResponse('success')


def details(request, id):
    rec1 = Recipe.objects.filter(id=id).select_related('author').first()
    if not rec1:
        return not_found_view(request=request, exception='')
    account = Account.objects.get(user=rec1.author)
    # .values_list('title', 'author', 'date', 'id', 'description')
    files = File.objects.filter(recipe=id)
    print("details files", files)
    liked_recipes_dict = find_what_liked(request)

    context = {
        "title": "",
        "recipe": rec1,
        "files": files,
        'account': account,
        "liked": liked_recipes_dict
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



def get_recipes_and_files():
    recipes = Recipe.objects.select_related("author").prefetch_related("images").all()
    print([(r.id, r.images.all()) for r in recipes])
    files =  {int(file.id): [ff.file for ff in file.images.all()]  for file in recipes}
    # print('gallery files', [list([ff.file for ff in v]) for f,  v in files.items()])
    print('gallery files', files)
    return recipes, files


def get_recipes_and_first_file(with_filter=False, page_number=0):
    if not with_filter:
        recipes = Recipe.objects.select_related("author").prefetch_related("images").order_by('-date').all()
    elif with_filter.get('author'):
        recipes = Recipe.objects.filter(author=with_filter.get('author')).select_related("author").prefetch_related("images").order_by('-date').all()
    else:
        title = with_filter.get('title')
        recipes = Recipe.objects.select_related("author").prefetch_related("images").filter(Q(title__icontains=title)|Q(description__icontains=title)).order_by('-date')
    
    # print([(r.id, r.images.first()) for r in recipes])
    total = len(recipes)
    page_paginator = Paginator(recipes,per_page=8)
    recipes_page_obj = page_paginator.get_page(page_number)

    files =  {int(file.id): [file.images.first().file if file.images.first() else None]  for file in recipes_page_obj}
    # print('gallery files', files)    

    return recipes_page_obj, files, total



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
            all_files = request.FILES.getlist('file')
            for img in all_files:
                File.objects.create(recipe=new_recipe, file=img)
            # if not all_files:
            #     File.objects.create(recipe=new_recipe, file='horizont.jpg')
           
            return redirect('/')
    else:
        form = RecipeAddForm()
    return render(request,'main/upload.html', {'form':form })


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    '''update'''
    model = Recipe
    fields = ['title','description','category']
    # fields = '__all__'
    template_name = 'main/upload.html'
    context_object_name = 'Recipe'
    # form_class = RecipeAddForm
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        current_object = self.object
        images = File.objects.filter(recipe=current_object)
        context['image_form'] = ImagesFormSet(instance=current_object)
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        author = User.objects.filter(id=self.request.user.id).first()
        recipe = Recipe.objects.filter(Q(author=author) & Q(id=self.object.pk))
        
        if not recipe.first(): # or self.request.user.id != recipe.author.id:
            messages.add_message(self.request, messages.WARNING, "Вы пытаетесь выполнить неверное действие")
            return redirect('main:main')
        return super(RecipeUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
     
            instance = form.save(commit=False)
            if instance.author != self.request.user:
                return self.form_invalid(form)
            # for img in request.FILES.getlist('account_image'):
            #     print(img)
            # form.save_m2m()
            rec = Recipe.objects.filter(id=self.object.pk).first()
            
            deleted_ids = []
            # for key in request.POST.keys():
            #     if key.startswith('images-'):
            current_object = Recipe.objects.get(id=request.POST['images-0-recipe'])

            for i in range(int(request.POST['images-TOTAL_FORMS'])): #удаление всех по галочкам
                field_delete =f'images-{i}-DELETE'
                field_image_id = f'images-{i}-id'
                if field_delete in request.POST and request.POST[field_delete] =='on':
                    image = File.objects.get(id=request.POST[field_image_id])
                    image.delete()
                    deleted_ids.append(field_image_id)
                    #тут же удалить картинку из request.FILES

            #Замена картинки
            for i in range(int(request.POST['images-TOTAL_FORMS'])):  # удаление всех по галочкам
                field_replace = f'images-{i}-file' #должен быть в request.FILES
                field_image_id = f'images-{i}-id'  #этот файл мы заменим
                if field_replace in request.FILES and request.POST[field_image_id] != '' and field_image_id not in deleted_ids:
                    image = File.objects.get(id=request.POST[field_image_id]) #
                    image.delete() #удаляем старый файл
                    for img in request.FILES.getlist(field_replace): #новый добавили
                        File.objects.create(recipe=current_object, file=img)
                    del request.FILES[field_replace] #удаляем использованный файл

            if request.FILES:
                for input_name in request.FILES:
                    for img in request.FILES.getlist(input_name):
                        File.objects.create(recipe=rec, file=img)
            return super().form_valid(form)
            
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('main:details', args=[self.object.pk])
    
    def form_invalid(self, form):
        'form is invalid'
        messages.add_message(self.request, messages.WARNING, "Вы пытаетесь выполнить неверное действие")
        return redirect('main:main')


class RecipeDeleteView(LoginRequiredMixin, View):
    '''DeleteView'''
    model = Recipe
    context_object_name = 'Recipe'
    pk_url_kwarg = 'pk'
    # success_url = reverse_lazy('main:main')

    def get_object(self):
        print('get_object')
        return get_object_or_404(Recipe, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        author = User.objects.filter(id=self.request.user.id).first()
        recipe = Recipe.objects.filter(Q(author=author) & Q(id=self.object.pk))
        
        if not recipe.first(): # or self.request.user.id != recipe.author.id:
            messages.add_message(self.request, messages.WARNING, "Вы пытаетесь выполнить неверное действие")
            return redirect('main:main')
        messages.add_message(self.request, messages.WARNING, f"Рецепт '{recipe.first().title}' удален")
        recipe.first().delete()
        return HttpResponse('success')

