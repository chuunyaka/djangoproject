from django.urls import path
from .views import IndexView
# from .views import upgrade_me

urlpatterns = [
    path('', IndexView.as_view()),
]