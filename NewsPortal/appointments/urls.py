from django.urls import path
from .views import index1  # Убедись, что представление index есть

urlpatterns = [
    path('', index1, name='index1'),
]
