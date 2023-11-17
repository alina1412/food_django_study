from django.shortcuts import render


from .models import Recipe, Product, description


def details(request):
    # Recipe.objects.all().first()
    # files
    rec1 = Recipe.objects.filter(id='1')

    
    # author = User.objects.get(id=request.user.id)
    # new_ = Recipe(author=author, title='gbrb', description='ftrbg')
    # new_.save()

    all_ = Recipe.objects.all()

    products = []

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
    products = [Product('Water efrege etbgetb', 'cake_baking_.jpg', description)]

    context = {'title': '', 
               'products': products,
               }
    return render(request, "main/recipe.html", context)
