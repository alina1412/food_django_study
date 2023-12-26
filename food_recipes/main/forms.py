from django import forms

from django.contrib.auth.models import User

from .models import File, Recipe


class ProfileForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=40, strip=True)
    gender = forms.CharField(label="Пол", max_length=10, required=False)
    age = forms.DecimalField(label="Возраст", min_value=1, max_value=200, 
                             max_digits=3, required=False)
    info = forms.CharField(label="Информация", 
                           widget=forms.Textarea(attrs={'cols': 40, 'rows': 7}), required=False, 
                           strip=True)




# from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, Select
# from .models import *

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# class FileFieldForm(forms.ModelForm):
#     file = MultipleFileField()
#     class Meta:
#         model = File

#         fields = ['file']

class RecipeAddForm(forms.ModelForm):
    file = MultipleFileField(required=False)

    class Meta:
        model = Recipe
        fields = ['title','description','category']


from django.forms import inlineformset_factory
ImagesFormSet = inlineformset_factory(Recipe, File, fields=("file",),extra=1,max_num=4,
    widgets={
        "image_field": MultipleFileField(required=False),
    })
# class RecipeForm(forms.ModelForm):
#     # account_image = forms.
#     nickname = forms.CharField(label="Имя", max_length=40, strip=True)
#     gender = forms.CharField(label="Пол", max_length=10, required=False)
#     birthdate = forms.DateField(label='Дата рождения', required=False)
#     age = forms.DecimalField(label="Возраст", min_value=1, max_value=200, 
#                              max_digits=3, required=False)
#     info = forms.CharField(label="Информация", 
#                            widget=forms.Textarea(attrs={'cols': 40, 'rows': 7}), required=False, 
#                            strip=True)
#     account_image = forms.ImageField(label='Аватар', required=False)

#     class Meta:
#         model = Recipe
#         fields = ['title','description','category']