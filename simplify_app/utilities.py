import uuid

from simplify_app.models import SimpleUrl

from django.dispatch import Signal
from django.core.signing import Signer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

signer = Signer()


def send_activation_notification(user, domain):
    host = 'http://' + domain
    context = {'user': user, 'host': host,
               'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    message = render_to_string('email/activation_letter_body.txt', context)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email, ],
        fail_silently=True
    )


user_registered = Signal()


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'], kwargs['domain'])


user_registered.connect(user_registered_dispatcher)


def create_simple_url(original_url, user):
    url = SimpleUrl.objects.filter(original_url=original_url)
    if url:
        return url[0].simple_url_id

    simple_url_id = str(uuid.uuid4())[:5]
    simple_url = SimpleUrl(original_url=original_url, user=user,
                           simple_url_id=simple_url_id)
    simple_url.save()
    return simple_url_id
