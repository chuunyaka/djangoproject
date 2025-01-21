from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewDetail

# urlpatterns = [
#    path('', NewsList.as_view()),
#    path('<int:pk>', NewDetail.as_view()),
# ]

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewDetail.as_view(), name='news_detail'),
]