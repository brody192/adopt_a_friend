from django.urls import path
from . import views

urlpatterns = [
    path('pawlink/<str:applicationId>/', views.lobby, name='lobby'),
    path('room/', views.room),
    path('get_token/', views.getToken),
]

# path('lobby/<str:applicationId/>', views.lobby, name='lobby'),