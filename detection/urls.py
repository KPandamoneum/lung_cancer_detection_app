from django.urls import path
from .views import home, home_async

urlpatterns = [
    path('', home, name='home'),
    path('home_async', home_async, name='home_async'),
]

