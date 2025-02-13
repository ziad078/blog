from django.urls import path
from .views import *
urlpatterns = [
    path('register/',register,name='register'),
    path('login/',signin,name='login'),
    path('signout/',signout,name='signout'),
    path('profile/',user_profile,name="user_profile"),
    path('delete-profile-img/',delete_profile_img,name="delete_profile_img"),
]
