from django.db import models

from django.contrib.auth.models import User

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
    birthdate = models.DateField(null=True)
    gender = models.CharField(choices=gender_choices,max_length=20)
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')
    #pip install pillow в терминале если нет библиотеки
    tags = models.ManyToManyField(to=Tag, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s account"


