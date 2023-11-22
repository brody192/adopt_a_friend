from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:applicationId>', views.home, name='chat'),
    path('<str:room>/', views.room, name='room'),
    path('chat/checkview/<str:applicationId>', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]