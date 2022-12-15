from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template


@shared_task(bind=True)
def send_mail(self, user, template, subject, context):

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
