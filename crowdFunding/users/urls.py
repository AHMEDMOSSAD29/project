# from django.conf.urls import url
from django.urls import path , include , re_path
from . import views
from django.contrib.auth import views as auth_views
from .views import  Dashboard,feature_it

app_name = "users"

urlpatterns = [
    path('profile/<int:uid>', views.userProfile , name='profile'),

    path('edit/<int:uid>', views.editProfile , name='edit'),
    path('delete/<int:uid>', views.deleteuser, name="delete"),
    path('signup',views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view\
        (template_name='users/logout.html'), name="logout"),
    path('dashboard/<int:pk>', Dashboard.as_view(), name='dashboard'),
    path('feature_id/', feature_it, name='feature_it'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),


]
