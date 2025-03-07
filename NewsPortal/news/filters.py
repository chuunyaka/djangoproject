from django.contrib.sites import models
from django_filters import CharFilter, FilterSet, DateFilter
from django.db import models
from django import forms
from .models import Post, Author

class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label="Название")
    author_username = CharFilter(field_name='author__user__username', lookup_expr='icontains', label="Автор")
    start_date = DateFilter(field_name="created_at", lookup_expr='gte',
                            label="Позже указанной даты", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author_username', 'start_date']

