# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from PIL import Image
from django_countries.fields import CountryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , verbose_name=("User Name"))
    email_confirmation = models.BooleanField(default=False , verbose_name=("Email"))
    phone_validation = RegexValidator(regex=r'^01[5|1|2|0][0-9]{8}$',
                                 message=" Please ,, Entered the Phone number in the format: '010|212|134|156'.")
    phone = models.CharField(max_length=11, null=True, blank=True , verbose_name=("Phone"))
    facebook =  models.URLField(null=True, blank=True , verbose_name=("FaceBook"))
    country = CountryField()
    birth_date = models.DateField(null=True, blank=True, verbose_name=("BirthDate"))
    user_image = models.ImageField(upload_to='images/users', default='images/users/R.jpg')

    def __str__(self):
        
        return f'{self.user.username}'
        img = Image.open(self.user_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_image.path)

     



    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.create(user=kwargs['instance'])


    post_save.connect(create_profile, sender=User)


