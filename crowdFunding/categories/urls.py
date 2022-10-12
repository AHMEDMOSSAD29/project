from django.urls import path
from . import views


urlpatterns = [
    path('create', views.CreateCategory.as_view(), name="createCategory")
]
