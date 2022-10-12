from django import forms
from projects.models import Category

class CategoryModelForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Category