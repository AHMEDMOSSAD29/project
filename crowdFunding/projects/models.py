# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from datetime import datetime
from users.models import Profile
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator

class Project(models.Model):
    title = models.CharField(max_length=45)
    details = models.TextField(max_length=3000)
    target = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=45)
    cat_icon = models.ImageField(upload_to='static/imgs/', default=True)

    def __str__(self):
        return str(self.name)


class ProjectPicture(models.Model):
    img_url = models.ImageField(upload_to='static/imgs/', verbose_name='Image')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=None, related_name='imgs')

    def __str__(self):
        return str(self.project.title)


class Comment(models.Model):
    content = models.TextField(max_length=3000, blank=False)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'comment by {self.user.user.username} on {self.project.title} project.')


class ProjectReport(models.Model):
    content = models.TextField(max_length=3000)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)


class CommentReport(models.Model):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)


class Donation(models.Model):
    amount = models.IntegerField()
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    value = models.IntegerField(default=1,
                                validators=[
                                    MaxValueValidator(100),
                                    MinValueValidator(1)
                                ])
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)

#
# class Data(models.Model):
#     title = models.CharField(max_length=100)
#     tags = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.first_name