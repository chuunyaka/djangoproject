from allauth.headless.urls import app_name
from django.urls import path
from .views import NewsSearch, NewsList, NewDetail, NewCreate, NewUpdate, NewDelete, ArticleCreate, ArticleDelete, \
    ArticleUpdate, CategoryListView, subscribe_to_category
from .views import upgrade_me
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.views import SignupView
app_name= 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewDetail.as_view(), name='new_detail'),
    path('create/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('categories/<int:pk>',CategoryListView.as_view(), name='category_list'),
    path('categories/<int:category_id>/subscribe', subscribe_to_category, name='subscribe_to_category'),

    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('login/',LoginView.as_view(template_name='news/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='news/logout.html'),name='logout'),
    path('signup/',SignupView.as_view(template_name='news/signup.html'),name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
]