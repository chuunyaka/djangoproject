from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.conf import settings

def notify_subscribers_on_create(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()
        subject = f'Новая статья в категории: {category}'
        current_site = Site.objects.get.current()
        message = f'Заголовок: {instance.title}\n\nТекст: {instance.text[:200]}...\n\nЧитай полностью: http://{current_site.domain}/news/{instance.id}/'

        for user in subscribers:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )