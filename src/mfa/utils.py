from django.http import HttpRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from .models import User, User2FALogs


def email_2fa_send(user: User, request: HttpRequest) -> User2FALogs:
    """sends 2FA challenge to user"""
    # generate challenge token
    challenge = User2FALogs(
        user=user
    )
    challenge.save()

    # First, render the plain text content.
    text_content = render_to_string(
        "mfa/emails/mfa.txt",
        context={
            "url": f"https://{request.get_host()}"
            f"{reverse('mfa:email_2fa_challenge', args=[challenge.token])}"
        },
    )

    # Secondly, render the HTML content.
    html_content = render_to_string(
        "mfa/emails/mfa.html",
        context={
            "user": user.intra,
            "url": f"https://{request.get_host()}"
            f"{reverse('mfa:email_2fa_challenge', args=[challenge.token])}"
        },
    )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        "merge-insertion-sort: login",
        text_content,
        settings.EMAIL_USER,
        [user.email,],
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return challenge
