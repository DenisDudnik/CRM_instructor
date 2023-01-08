from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django.utils import timezone

from courses.models import Lesson


@shared_task(bind=True)
def send_mail_to_user(self, user, template, subject, context):

    message = get_template(template).render(context)
    mail_subject = subject
    to_email = user.email

    msg = EmailMessage(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
    )

    msg.content_subtype = "html"
    msg.send()

    return str(to_email)


@shared_task
def lesson_notifications():
    lessons = Lesson.objects.all()
    now = timezone.now()
    two_days_ahead = now + timedelta(days=2)

    for lesson in lessons:
        if now < lesson.date < two_days_ahead:
            if (lesson.date - now).days > 0:
                msg = f'Урок {str(lesson)} из "{lesson.course}" курса\
                     начинается через {(lesson.date - now).days} дня(день).'
            else:
                msg = f'Урок {str(lesson)} из "{lesson.course}" курса начинается сегодня.'
            send_mail('Напоминание о начале урока',
                      msg,
                      settings.EMAIL_HOST_USER,
                      list(lesson.users.all().values_list('email', flat=True)))
