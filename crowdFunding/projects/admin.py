# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from projects.models import *

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Comment)

admin.site.register(Donation)
admin.site.register(Rate)
admin.site.register(CommentReport)
admin.site.register(ProjectReport)
admin.site.register(ProjectPicture)
