from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
 

from .models import Recipe, Category, File


class RecipeAdmin(ModelAdmin):
    list_display = ['pk', 'title', 'author', 'show_description', 'date']
    list_filter = ['title', 'author', 'date', 'category', 'votes']
    search_fields = ['title__icontains']
   
    readonly_fields=('votes', 'author')

    def show_description(self, obj):
        return obj.description[:40] + '...'
    
    def __str__(self) -> str:
        return f'{self.title} {str(self.date[:16])}'
    
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

         
class CategoryAdmin(ModelAdmin):
    list_display = ['pk', 'food_type']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class FileAdmin(ModelAdmin):
    list_display = ['recipe', 'image_tag']
    list_filter = ['recipe']

    def __str__(self) -> str:
        return f'{self.filename}'
    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)