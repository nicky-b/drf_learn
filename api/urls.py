from django.urls import path, include
from home.views import index, person

urlpatterns = [
    path('index/', index),
    path('person/', person),

]