from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from .models import Post, Category

@shared_task
def send_weekly_news():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        category_posts = posts.filter(category=category)

        if category_posts.exists():
            for user in subscribers:
                html_content = render_to_string(
                    'news/weekly_email.html',
                    {
                        'username': user.username,
                        'posts': category_posts,
                        'category': category.name
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'Еженедельная подборка новостей по категории {category.name}',
                    body='',
                    from_email='viktoriakasenceva95@yandex.ru',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()