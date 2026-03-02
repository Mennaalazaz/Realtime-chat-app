from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('checkview', views.checkview, name='checkview'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
    path('getMessages/<str:room_name>/', views.getMessages, name='getMessages'),
    path('<str:room_name>/', views.room, name='room'),
]