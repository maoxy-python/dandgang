from django.contrib import admin
from django.urls import path, include

from demo1 import views

urlpatterns = [
    path('register/', views.register_form),
    path('user_register/', views.user_register),
    path('user_confirm/', views.email_confirm),
]
