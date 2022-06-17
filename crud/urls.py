from django.contrib import admin
from django.urls import path, include
from .views import Home, MyPost, DetailPost,create_protocol,create_process ,UpdatePost, DeletePost

app_name='crud'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('mypost/', MyPost.as_view(), name='mypost'),
    path('detail/<int:pk>', DetailPost.as_view(), name='detail'),
    path('detail/<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('create/', create_protocol, name='create'),  
    path('create/<int:pk>', create_process, name='create2'),  
]
