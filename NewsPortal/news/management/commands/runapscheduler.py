import logging
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category

logger = logging.getLogger(__name__)


def weekly_mail_job():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week, post_type=Post.NEWS)
    categories = Category.objects.all()

    for category in categories:
        posts_in_cat = posts.filter(category=category)
        if not posts_in_cat.exists():
            continue

        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        for user in subscribers:
            html_content = render_to_string(
                'news/weekly_email.html',
                {
                    'username': user.username,
                    'posts': posts_in_cat,
                    'category': category,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Еженедельная подборка новостей в категории "{category.name}"',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f'Отправлена рассылка {user.email}')


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs weekly mail scheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_mail_job,
            trigger=CronTrigger(day_of_week="sun", hour="12", minute="00"),
            id="weekly_mail_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mail_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added cleanup job.")

        try:
            logger.info("Starting weekly mail scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info("Scheduler stopped.")
