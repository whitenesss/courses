from datetime import timedelta, timezone
from celery import Celery
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from cours.models import Subscription
from users.models import User


@shared_task
def notify_subscribers(well_id):
    """Рассылка пользователям на обновления контента курса"""
    subscriptions = Subscription.objects.filter(sab_well=well_id)

    for subscription in subscriptions:
        user = subscription.seb_user
        send_mail(
            'Новый курс на платформе',
            f'На платформе появился новый курс: {subscription.sab_well.title}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def check_last_login():
    """Переодическая задача для проверки не активных пользователей """
    print('Запуск задачи check_last_login')
    inactive_period = timedelta(days=30)
    threshold_date = timezone.now() - inactive_period
    inactive_users = User.objects.filter(last_login__lt=threshold_date)

    for user in inactive_users:
        if user.is_active:
            user.is_active = False
            user.save()
            print(f'пользователь {user.email} отключен')
