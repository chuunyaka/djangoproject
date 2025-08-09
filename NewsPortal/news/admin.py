from django.contrib import admin
from .models import Author, Category, Post, Comment

def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
nullify_rating.short_description = "Обнулить рейтинг"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_categories', 'rating', 'created_at')
    list_filter = ('category', 'author', 'created_at')
    search_fields = ('title', 'author__user__username', 'category__name')
    actions = [nullify_rating]

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])
    get_categories.short_description = 'Категории'

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

# from django.contrib import admin
# from .models import Author, Category, Post, Comment
#
# def nullify_rating(modeladmin, request, queryset):
#     queryset.update(rating=0)
# nullify_rating.short_description = "Обнулить рейтинг"
#
# # ✅ Кастомизация отображения постов
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'category', 'rating', 'created_at')  # покажи ключевые поля
#     list_filter = ('category', 'author', 'created_at')  # фильтры справа
#     search_fields = ('title', 'author__username', 'category__name')  # строка поиска
#     actions = [nullify_rating]  # доступные действия
#
# admin.site.register(Author)
# admin.site.register(Category)
# admin.site.register(Post)
# # admin.site.register(PostCategory)
# admin.site.register(Comment)
# Register your models here.

