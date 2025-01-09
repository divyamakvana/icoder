from django.contrib import admin
from .import views
from django.urls import path 

urlpatterns = [
   
   
    # API to post comment
    path('postComment', views.postComment, name="postComment"), 
    
    path('', views.bloghome, name='bloghome' ),
    path('<str:slug>', views.blogPost, name='blogpost' ),
    
   
   
]