from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.urls import reverse
 

from .models import Account, Tag


class AccountAdmin(ModelAdmin):
    list_display = ['pk', 'user', 'nickname', 'gender']
    list_filter = ['user', 'gender']
    list_display_links = ['pk', 'nickname']

    def __str__(self) -> str:
        return f'{self.title} {str(self.date[:16])}'
    
    def get_absolute_url(self):
        return reverse('account', args=[self.pk])
    


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['id', 'title', 'status']
    list_filter = ['title', 'status']
    list_display_links = ['id']
    list_editable = ['title']

    def __str__(self) -> str:
        return f'{self.title}'
   

admin.site.register(Account, AccountAdmin)
# admin.site.register(Tag, TagAdmin)
# admin.site.register(File, FileAdmin)
from django.contrib.auth.models import Group
def make_editor(modeladmin, request, queryset):
    group = Group.objects.get(name='Editors')
    ungroup = Group.objects.get(name='Normal')
    for user in queryset:
        user.groups.add(group)
        user.groups.remove(ungroup)
        user.is_staff = True
        user.save()

make_editor.short_description = "Утвердить редактора"


from typing import Set

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'is_superuser',	'username',	'first_name',	'last_name',	'email',
                    	'is_staff',	'is_active',	'last_login',	'date_joined']
    list_display_links = ['id']
    actions = [make_editor]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
    
    class Meta:
        # ordering = ['itle','status']
        verbose_name= 'Пользователь (User)'
        verbose_name_plural='Пользователи (Users)'


