from datetime import timedelta
import json
import base64

import jwt

from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from .models import User, User2FALogs


@require_GET
def email_2fa_challenge(request):
    """checks challenge code and generates JWT"""
    # check if user has finished OAuth login
    token = request.COOKIES.get("waiting-for-2fa")
    if not token:
        # TODO handle error (not from OAuth)
        raise Exception
    if not request.GET.get("challenge"):
        # TODO handle error (not from email)
        raise e

    try:
        payload = jwt.decode(token, settings.JWT_SECRET,
                             algorithms=[settings.JWT_ALGORITHM])
        user_id, challenge_id = payload.get(
            'user_id'), payload.get('challenge_id')
        if not user_id:
            # TODO handle error (wrong cookie)
            raise Exception
    except jwt.PyJWTError as e:
        # TODO handle error
        raise e

    # check challenge code
    user = User.objects.get(pk=user_id)
    challenge = User2FALogs.objects.filter(user=user).order_by('-pk').first()
    if challenge is None:
        # TODO handle error (there was no oauth request)
        raise Exception
    if challenge.pk != challenge_id:
        # TODO handle error (this challenge is expired)
        raise Exception
    # TODO make 'easy mode' for evaluation
    if str(challenge.token) != request.GET.get('challenge'):
        # TODO handle error (wrong challenge code)
        ct = challenge.token
        rt = request.GET.get('challenge')
        raise Exception
    challenge.login = timezone.now()
    challenge.save()

    # create JWT and return
    oauth = user.useroauthinformation
    payload = {
        'user_id': user.pk,
        'username': user.intra,
        'exp': min(
            timezone.now() +
            timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
            oauth.token_expire
        ).timestamp()
    }
    token = jwt.encode(payload, settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)
    resp = redirect('/')
    resp.set_cookie('ford-johnson-sort', token, secure=True, httponly=True)
    resp.set_cookie('merge-insertion-sort',
                    base64.urlsafe_b64encode(
                        json.dumps(payload).encode()
                    ).rstrip(b'=').decode(),
                    secure=True, httponly=False)
    resp.delete_cookie('waiting-for-2fa')
    return resp
