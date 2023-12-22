from typing import Any

from django.db.models import Count, Avg, Max
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from django.urls import reverse_lazy, reverse


from .models import Account
# from main.forms import ProfileForm
from .forms import AccountForm, LoginForm, RegisterForm


class AccountDetailView(DetailView):
    model = Account
    template_name = 'users/user_detail.html'
    context_object_name = 'profile'
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['username'] = Account.objects.filter
        return context


class UserAccountView(LoginRequiredMixin, UpdateView):
    '''users/user/1'''
    model = Account
    # fields = ['nickname','gender', 'birthdate','age', 'info', 'account_image']
    # fields = '__all__'
    template_name = 'users/account.html'
    context_object_name = 'profile'
    form_class = AccountForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = AccountForm()
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.id != self.object.pk:
            messages.add_message(self.request, messages.WARNING, "Вы пытаетесь выполнить неверное действие")
            return redirect('users:account', self.request.user.id)
        return super(UserAccountView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            # if self.request.user == thisArticle.author:
            instance = form.save(commit=False)
            if instance.user != self.request.user:
                return self.form_invalid(form)
            # for img in request.FILES.getlist('account_image'):
            #     print(img)
            return super().form_valid(form)
            
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('users:account', kwargs={'pk': self.object.pk})
    
    def form_invalid(self, form):
        'form is invalid'
        messages.add_message(self.request, messages.WARNING, "Вы пытаетесь выполнить неверное действие")
        return redirect('main:main')


def logout_view(request):
    logout(request)
    return redirect('main:main')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Вы уже залогинились на сайте. Хотите создать еще один аккаунт?')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, "title": "Регистрация", "btn_text": "Регистрация"})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Normal')
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request, user)

            new_ = Account(user=user, nickname=username)
            new_.save()

            messages.success(request, f'Account created for {username}')

            return redirect('main:main')

        return render(request, self.template_name, {'form': form, "title": "Регистрация", "btn_text": "Регистрация"})


def loginView(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # DEBUG
            acc = Account.objects.filter(user=user).first()
            if not acc:
                new_ = Account(user=user, nickname=username)
                new_.save()

            return redirect('main:main')
           
        print(form.errors.as_data())
        
        context = {"title": "Войти", "btn_text": "Войти", 'form': form, 'messages':get_messages(request) }
        return render(request, "users/login.html", context)
    else:
        if request.user.is_authenticated:
            messages.add_message(request, messages.SUCCESS, 'Вы уже залогинились на сайте')
            # messages.success(request, 'Вы уже залогинились на сайте', extra_tags='success')
            return redirect('main:main')
   
    # log_dict['type'] = 'login'
    context = {"title": "Войти", "btn_text": "Войти",  'form': LoginForm(), 'messages':get_messages(request) }
    return render(request, "users/login.html", context, )
