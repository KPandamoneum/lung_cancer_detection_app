from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home_async', views.home_async, name='home_async'),
]

