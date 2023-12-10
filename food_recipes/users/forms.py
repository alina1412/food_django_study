from django import forms
from django.contrib.auth.forms import AuthenticationForm,\
                                      UserCreationForm
from django.contrib.auth.models import User

from .models import Account


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=200,
               widget=forms.TextInput(attrs={"class":"form_field",
                                             'autofocus': True}))

    password = forms.CharField(label="Пароль", 
               widget=forms.PasswordInput(attrs={"class":"form_field"}))

    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", max_length=200, min_length=4,
               widget=forms.TextInput(attrs={"class":"form_field",
                                             'autofocus': True}))

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"form_field",
                                          "autocomplete": "new-password"}))

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class":"form_field",
                                          "autocomplete": "new-password"}),
                                          strip=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AccountForm(forms.ModelForm):
    # account_image = forms.
    nickname = forms.CharField(label="Имя", max_length=40, strip=True)
    gender = forms.CharField(label="Пол", max_length=10, required=False)
    birthdate = forms.DateField(label='Дата рождения', required=False)
    age = forms.DecimalField(label="Возраст", min_value=1, max_value=200, 
                             max_digits=3, required=False)
    info = forms.CharField(label="Информация", 
                           widget=forms.Textarea(attrs={'cols': 40, 'rows': 7}), required=False, 
                           strip=True)
    account_image = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = Account
        fields = ['nickname','gender', 'birthdate','age', 'info', 'account_image']