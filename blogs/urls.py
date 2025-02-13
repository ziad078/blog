from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('blog_details<int:pk>/', blog_details, name='blog_details'),
    path('cat_blog/<str:slug>/', cat_blog, name='cat_blog'),
    path('create_comment<int:id>/', create_comment, name='create_comment'),
    path('delete_comment/', delete_comment, name='delete_comment'),
    path('edit_blog/', edit_blog, name='edit_blog'),  
    path('edit_blog<int:id>/', edit_blog, name='edit_blog'),  
    path('delete_blog<int:id>/', delete_blog, name="delete_blog"),  
    path('search/', search, name="search"),  
]
