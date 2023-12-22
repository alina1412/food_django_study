from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

from main.models import Recipe


class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title','status']
        verbose_name= 'Тег'
        verbose_name_plural='Теги'


class Account(models.Model):
    gender_choices= (('M','Male'),
                     ('F','Female'),
                     ('N/A','Not answered'))
    user = models.OneToOneField(User,on_delete=models.CASCADE,
                                primary_key=True)
    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=gender_choices,max_length=20)
    age = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')
    #pip install pillow в терминале если нет библиотеки
    tags = models.ManyToManyField(to=Tag, blank=True)
    likes_recipes = models.ManyToManyField(Recipe, through="VotesConnection")
    
    def __str__(self):
        return f"{self.user.username}'s account"

    def get_absolute_url(self):
        return reverse('account', args=[self.pk])

    class Meta:
        # ordering = ['itle','status']
        verbose_name= 'Аккаунт (Account)'
        verbose_name_plural='Аккаунты'


class VotesConnection(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
