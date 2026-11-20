from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('reservar/', views.crear_reserva, name='crear_reserva'),
    path('reserva-exitosa/', views.reserva_exitosa, name='reserva_exitosa'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
]
