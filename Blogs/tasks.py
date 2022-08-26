from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from NewsApi_Blogs import settings

@shared_task(bind=True)
def send_mail_func(self, name, message):
    current_user = name
    users = get_user_model().objects.get(email=current_user)
    mail_subject = "Hi! {}".format(users.username)
    to_email = users.email
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done"