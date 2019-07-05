from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', custom_login,  name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', user_register, name='sign_up'),
    path('update/', user_update, name='update'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('', index, name='home'),
]
