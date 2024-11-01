from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('homeregister', views.homeregister, name="homeregister"),
    path('register', views.register, name="register"), 
    path('givevote', views.givevote, name="givevote"),
]