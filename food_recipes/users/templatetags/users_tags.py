from django import template
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="has_group")
@stringfilter
def has_group(user, group_name):
    user = User.objects.get(username=user)
    return user.groups.filter(name=group_name).exists()
