from django.urls import path
from .views import *


urlpatterns =[
    path('',Register,name='register'),
    path('login/',Login,name='login'),
    path('logout/', Logout, name='logout'),
    path('dashboard/',Dashboard,name='dashboard')
]