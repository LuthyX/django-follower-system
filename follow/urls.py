from django.urls import path
from . import views
from django.contrib import admin

urlpatterns =[
path('', views.index, name='index'),
path('register', views.register, name='register'),
path('login', views.login, name='login'),
path('logout', views.logout, name = 'logout'),
path('followers_count',views.followers_count, name='followers_count')
]