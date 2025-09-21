from django.urls import path
from .views import *


urlpatterns =[
    path('',Register,name='reqister'),
    path('login/',Login,name='login'),
    path('dashboard/',Dashboard,name='dashboard')
]