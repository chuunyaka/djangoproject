import django_filters
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.timezone import now
import django_filters
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
            post_rating = 3 * sum(post.rating for post in self.post_set.all())

            comment_rating = sum(comment.rating for comment in self.user.comment_set.all())

            post_comments_rating = sum(comment.rating for comment in Comment.objects.filter(post__author=self))

            self.rating = post_rating + comment_rating + post_comments_rating
            self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique = True)
    subscribers = models.ManyToManyField(User, blank=True, related_name= "categories")
    def __str__(self):
        return self.name

class Post(models.Model):
    # objects = None
    ARTICLE = 'AR'
    NEWS = 'NW'
    TYPES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    )

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices= TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through= 'PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Передаем аргументы корректно

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self):
        return f'{self.title}: {self.text[:10]}'  # Используем title вместо name


    def get_absolute_url(self):
        return reverse('news:new_detail', kwargs={'pk': self.pk})
        # return reverse('new_detail', args=[str(self.id)])

    def send_notification(self):
        for category in self.category.all():
            for user in category.subscribers.all():
                subject = self.title
                html_content = render_to_string(
                    'news/email_notification.html',
                    {
                        'username': user.username,
                        'title': self.title,
                        'text_preview': self.text[:50],
                        'category': category.name,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='Здравствуй, {}. Новая статья в твоём любимом разделе!'.format(user.username),
                    from_email='viktoriakasenceva95@yandex.ru',
                    to=[user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




