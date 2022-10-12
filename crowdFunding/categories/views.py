from django.shortcuts import render
from projects.models import Category
from categories.forms import CategoryModelForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(login_required, name='dispatch')
class CreateCategory(CreateView):
    form_class = CategoryModelForm
    template_name = 'categories/createCategory.html'
    success_url = '/'