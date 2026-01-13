# core/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_welcome_email_task(self, user_id):
    from django.contrib.auth.models import User
    
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            'Welcome to EventTribe',
            f'Welcome {user.username}! Thank you for registering.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as exc:
        # Retry the task
        raise self.retry(exc=exc, countdown=60)