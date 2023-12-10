from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.views.generic import DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse

from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import logout, authenticate, login


from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max
from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView



from .models import Account
# from main.forms import ProfileForm
from .forms import AccountForm, LoginForm, RegisterForm

def index(request):
    # author = User.objects.get(id=request.user.id)

    a1 = Account.objects.all().first()
    # files
    print(a1.user.username, a1.birthdate, a1.nickname, a1.gender, [tag.title for tag in a1.tags.all()], '----')

    # acc2 = Account.objects.filter(user_id='1').first()

    # print(acc2.nickname, '----')

    acc = Account.objects.get(user=1)
    print(acc.tags.all())
    # acc3 = Account.objects.get(user=acc2.user)
    # print(acc3.email, '----')


    # all_ = Recipe.objects.all()
    return render(
        request, "users/account.html"
    )


class UserDetailView(DetailView):
    model = Account
    template_name = 'users/account.html'
    context_object_name = 'profile'


class UserAccountView(UpdateView):
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            # form.instance.created_by = self.request.user
            return super().form_valid(form)
            # return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('users:account', kwargs={'pk': self.object.pk})


# class UserUpdateView(UpdateView):
#     model = Account
#     template_name = 'users/account.html'
#     fields = ['nickname','birthdate','gender','tags', 'account_image']

#     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         print(request.FILES)
#         return super().post(request, *args, **kwargs)


# success_url = reverse_lazy('news_index')



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
            form.save()

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
