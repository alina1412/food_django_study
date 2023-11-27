from django.shortcuts import render

from django.contrib.auth.models import User
from .models import Recipe2, description


def one(request):
    # Recipe.objects.all().first()
    # files

    
    author = User.objects.get(id=request.user.id)
    new_ = Recipe2(author=author, title='gbrb', description='ftrbg')
    new_.save()

    rec1 = Recipe2.objects.filter(id='1')
    print(rec1)

    all_ = Recipe2.objects.all()
    print(all_)

    products = [rec1]

    # for x in all_:
    #     obj_ = {}
    #     for key_, value in x.get_fields:
    #         obj_[key_] = value
    #     obj_['img'] = ''
    #     products.append(obj_)
    # [tuple(x) ]
    # dict_ = [dict(rec) for rec in all]
    # for rec in dict_:
    #     dict_['img'] = ''

    # products = [Recipe('Water efrege etbgetb', 'cake_baking_.jpg', '1')]
    # products = [Product('Water efrege etbgetb', 'cake_baking_.jpg', description)]

    context = {'title': '', 
               'products': products,
               }
    return render(request, "recipes/recipe.html", context)
