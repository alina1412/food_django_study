from django.shortcuts import render

from django.contrib.auth.models import User
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
