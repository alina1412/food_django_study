from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.urls import reverse
 

from .models import Account, Tag


class AccountAdmin(ModelAdmin):
    list_display = ['user', 'gender', 'nickname']
    list_filter = ['user', 'gender']

    def __str__(self) -> str:
        return f'{self.title} {str(self.date[:16])}'
    
    # def get_absolute_url(self):
    #     return reverse('detail', args=[str(self.slug)])
    
    # class Meta:
    #     ordering = ['date']
    #     verbose_name = 'Recipe'
    #     verbose_name_plural = 'Recipes'


class TagAdmin(ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['title', 'status']

    def __str__(self) -> str:
        return f'{self.title}'
   

admin.site.register(Account, AccountAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(File, FileAdmin)