import os
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, UpdateView
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import PostForm
from .filters import PostFilter
from .models import Post
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class NewDetail(DetailView):
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'

class NewCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'new_edit.html'
    permission_required = 'news.add_post'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to create a post.")

        # Проверка на группу authors
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("You do not have permission to create a post.")

        return super().dispatch(request, *args, **kwargs)

class NewUpdate(LoginRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to edit a post.")

        # Проверка на группу authors
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("You do not have permission to edit this post.")

        return super().dispatch(request, *args, **kwargs)

class NewDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')

class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def news_search(request):
    news = Post.objects.all()
    filterset = PostFilter(request.GET, queryset=news)  # Применяем фильтр
    return render(request, 'news_search.html', {'filterset': filterset, 'news': filterset.qs})


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    permission_required = 'news.add_post'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to create a post.")

        # Проверка на группу authors
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("You do not have permission to create a post.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE  # Используем правильный тип
        post.save()
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to edit a post.")

        # Проверка на группу authors
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("You do not have permission to edit this post.")

        return super().dispatch(request, *args, **kwargs)

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

def index(request):
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'protect', 'index.html')
    print(f"Ищется шаблон: {template_path}")
    return render(request, 'protect/index.html')

class AddNew(PermissionRequiredMixin, View):
    permission_required = ('news.add_new',)

class ChangeNew(PermissionRequiredMixin, View):
    permission_required = ('news.change_new',)
