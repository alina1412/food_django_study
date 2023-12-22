from django.template.defaulttags import register
from django.db.models.fields.files import ImageFieldFile, FileField



@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict): 
        res = dictionary.get(key, None)
    else:
        res = None
    return res


@register.filter
def get_img(dictionary, key):
    if isinstance(dictionary, dict): 
        res = dictionary.get(key, (None,))
    else:
        res = [None]
    if not res[0]:
        res = [ImageFieldFile(instance=None, field=FileField(), name='import/horizont.jpg')]
    return res


from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)


from main.models import User
from users.models import Account

@register.filter(name='get_account_id')
def get_account_id(user):
    acc = Account.objects.get(user=user)
    return acc.pk
