from django import forms

from django.contrib.auth.models import User



class ProfileForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=40, strip=True)
    gender = forms.CharField(label="Пол", max_length=10, required=False)
    age = forms.DecimalField(label="Возраст", min_value=1, max_value=200, 
                             max_digits=3, required=False)
    info = forms.CharField(label="Информация", 
                           widget=forms.Textarea(attrs={'cols': 40, 'rows': 7}), required=False, 
                           strip=True)



