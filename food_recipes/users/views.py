from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.views.generic import DetailView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Account

def index(request):
    # author = User.objects.get(id=request.user.id)
    # new_ = Account(user=author, nickname='ftrbg')
    # new_.save()

    a1 = Account.objects.all().first()
    # files
    print(a1.user.username, a1.birthdate, a1.nickname, a1.gender, [tag.title for tag in a1.tags.all()], '----')

    # acc2 = Account.objects.filter(user_id='1').first()

    # print(acc2.nickname, '----')

    u1 = Account.objects.get(user=1)
    print(u1.tags.all())
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


class UserUpdateView(UpdateView):
    model = Account
    template_name = 'users/account.html'
    fields = ['nickname','birthdate','gender','tags', 'account_image']

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print(request.FILES)
        return super().post(request, *args, **kwargs)


# success_url = reverse_lazy('news_index')