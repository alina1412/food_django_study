from django.contrib import admin
from django.urls import reverse
 

from .models import Recipe, Category


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'date', 'category']
    list_filter = ['title', 'author', 'description', 'date', 'category']

    def __str__(self) -> str:
        return f'{self.title} {str(self.date[:16])}'
    
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

         
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['food_type']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)