from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.timezone import now
from django.core.mail import send_mail

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
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_new_post_email(self)

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
        return reverse('new_detail', args=[str(self.id)])



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

def send_new_post_email(post):
    subscribers = post.category.subscribers.all()
    subject = post.title
    message = f"Здравствуй, {post.title[:50]}... Новая статья в твоём любимом разделе!"
    html_message = f"<h1>{post.title}</h1><p>{post.content[:50]}...</p>"

    for user in subscribers:
        send_mail(
            subject,
            message,
            'from@example.com',
            [user.email],
            html_message=html_message,
        )



