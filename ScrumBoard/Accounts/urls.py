from django.contrib import admin
from django.urls import path
from ScrumBoard import views
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profilo/', views.profilo),
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name = 'register'),

]