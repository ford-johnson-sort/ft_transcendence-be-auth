from urllib.parse import urlencode
from datetime import timedelta

import jwt
import requests

from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from mfa.utils import email_2fa_send

from .models import User, UserOauthInformation


@require_GET
def oauth_index(request):
    """checks for user cookie, and redirects to 42 API if needed"""
    # check if user has authenticated
    token = request.COOKIES.get("ford-johnson-sort")
    if token:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET,
                                 algorithms=[settings.JWT_ALGORITHM])
            current_username = payload.get("username")
            if current_username and User.objects.filter(name=current_username).first() != None:
                return redirect('/')
        except jwt.PyJWTError:
            pass

    # send callback
    base_url = 'https://api.intra.42.fr/oauth/authorize'
    query_params = {
        'client_id': settings.OAUTH_UID,
        'redirect_uri': f"https://{request.get_host()}{reverse('oauth:oauth_callback')}",
        'response_type': 'code'
    }
    return redirect(f'{base_url}?{urlencode(query_params)}')

# TODO: use refresh token


@require_GET
def oauth_callback(request):
    """handles OAuth callback from 42 API"""
    # fetch token from 42 API
    try:
        token = requests.post(
            url='https://api.intra.42.fr/oauth/token',
            data={
                'code': request.GET['code'],
                'client_id': settings.OAUTH_UID,
                'client_secret': settings.OAUTH_SECRET,
                'grant_type': 'authorization_code',
                'redirect_uri': f"https://{request.get_host()}{request.path}"
            },
            timeout=5
        )
    except requests.exceptions.Timeout as e:
        return redirect('/?error=oauth-timeout')
    if token.status_code != 200:
        return redirect('/?error=oauth-error')
    token = token.json()

    # fetch user information from 42 API
    try:
        profile = requests.get(
            url='https://api.intra.42.fr/v2/me',
            headers={
                'Authorization': f"Bearer {token['access_token']}"
            },
            timeout=5
        )
    except requests.exceptions.Timeout as e:
        return redirect('/?error=oauth-timeout')
    if profile.status_code != 200:
        return redirect('/?error=oauth-error')
    profile = profile.json()

    # write user information to Database
    user = User.objects.filter(intra=profile['login']).first()
    new_user = user is None
    if new_user:
        user = User(
            intra=profile['login'],
            name=profile['usual_full_name'],
            email=profile['email'],
        )
        user.save()
        user_oauth = UserOauthInformation(
            user=user,
            token_access=token['access_token'],
            token_refresh=token['refresh_token'],
            token_expire=timezone.now() +
            timedelta(seconds=token['expires_in'])
        )
    else:
        user_oauth = UserOauthInformation.objects.get(user=user)
        user_oauth.token_access = token['access_token']
        user_oauth.token_refresh = token['refresh_token']
        user_oauth.token_expire = timezone.now() + \
            timedelta(seconds=token['expires_in'])
    user_oauth.save()

    # send 2FA email to user
    challenge = email_2fa_send(user_oauth.user, request)

    # set temporary cookie then return
    payload = {
        'user_id': user_oauth.user.pk,
        'challenge_id': challenge.pk
    }
    token = jwt.encode(payload, settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)
    resp = redirect('/')
    resp.set_cookie('waiting-for-2fa', token, secure=True, httponly=True)
    return resp
