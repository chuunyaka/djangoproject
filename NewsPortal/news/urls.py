from django.urls import path
# Импортируем созданное нами представление
from .views import NewsSearch, NewsList, NewDetail, NewCreate, NewUpdate, NewDelete, ArticleCreate, ArticleDelete, ArticleUpdate

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewDetail.as_view(), name='new_detail'),
    path('create/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),


    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    ]
