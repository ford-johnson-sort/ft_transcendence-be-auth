import uuid

from .models import User, User2FALogs


def email_2fa_send(user: User) -> User2FALogs:
    """sends 2FA challenge to user"""
    # generate challenge token
    challenge = User2FALogs(
        user=user
    )
    challenge.save()

    # TODO: send email

    return challenge
