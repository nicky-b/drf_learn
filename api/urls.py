from django.urls import path, include
from home.views import index, person, login

urlpatterns = [
    path('index/', index),
    path('person/', person),
    path('login', login),
]