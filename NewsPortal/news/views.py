import os
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pyexpat.errors import messages
from unicodedata import category

from .forms import PostForm
from .filters import PostFilter
from .models import Post, Category
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user

        categories = post.category.all()
        category_subscriptions = {}
        for category in categories:
            category_subscriptions[category.id] = user in category.subscribers.all()

        context['categories'] = categories
        context['category_subscriptions'] = category_subscriptions
        return context


class NewCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = 'news.add_post'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to create a post.")

        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("You do not have permission to create a post.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.send_notification()
        return response


class NewUpdate(LoginRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'new_edit.html'
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to edit a post.")

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
    filterset = PostFilter(request.GET, queryset=news)
    return render(request, 'news_search.html', {'filterset': filterset, 'news': filterset.qs})


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    permission_required = 'news.add_post'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to create a post.")

        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("You do not have permission to create a post.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE
        post.save()
        return super().form_valid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.send_notification()
        return response


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    permission_required = 'news.change_post'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You need to be logged in to edit a post.")

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

class CategoryListView(ListView):
    model = Category
    template_name = ("news/category_list.html")
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('- created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

    # return redirect('category_detail', pk=category.id)



# @login_required
# def subscribe(request, pk):
#     print(f"subscribe view called for user {request.user} and category {pk}")
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(request.user)
#     message = 'Вы успешно подписались на рассылку новостей категории'
#     return render(request, 'news/subscribe.html', {'category': category, 'message': message})

# 2 def subscribe(request, pk):
#     category = get_object_or_404(Category, id=pk)
#     user = request.user
#
#     if user not in category.subscribers.all():
#         category.subscribers.add(user)
#         message = 'Вы успешно подписались на рассылку новостей категории'
#     else:
#         message = 'Вы уже подписаны на эту категорию'
#
#     return render(request, 'news/subscribe.html', {'category': category, 'message': message})

#1 def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#
#     message = 'Вы успешно подписались на рассылку новостей категории'
#     return render(request,'news/subscribe.html', {'category': category, 'message': message})


