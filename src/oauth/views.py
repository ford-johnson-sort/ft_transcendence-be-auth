from urllib.parse import urlencode
from datetime import timedelta

import jwt
import requests
import json
import base64

from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from .models import User, UserOauthInformation


def oauth_index(request):
    """checks for user cookie, and redirects to 42 API if needed"""
    # TODO: check user has already authenticated
    base_url = 'https://api.intra.42.fr/oauth/authorize'
    query_params = {
        'client_id': settings.OAUTH_UID,
        'redirect_uri': f"https://{request.get_host()}{reverse('oauth:oauth_callback')}",
        'response_type': 'code'
    }
    return redirect(f'{base_url}?{urlencode(query_params)}')

# TODO: use refresh token


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
        # TODO handle error
        raise e
    if token.status_code != 200:
        # TODO handle error
        raise Exception
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
        # TODO handle error
        raise e
    if profile.status_code != 200:
        # TODO handle error
        raise Exception
    profile = profile.json()

    # write user information to Database
    user_oauth = User.objects.filter(intra=profile['login']).first()
    new_user = user_oauth is None
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
        user_oauth.token_access = token['access_token']
        user_oauth.token_refresh = token['refresh_token']
        user_oauth.token_expire = timezone.now() + \
            timedelta(seconds=token['expires_in'])
    user_oauth.save()

    # create JWT and return
    payload = {
        'user_id': user_oauth.pk,
        'username': user_oauth.intra,
        'exp': (timezone.now() + timedelta(seconds=min(settings.JWT_EXP_DELTA_SECONDS, token['expires_in']))).timestamp()
    }
    token = jwt.encode(payload, settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)
    resp = redirect('/')
    resp.set_cookie('ford-johnson-sort', token, secure=True, httponly=True)
    resp.set_cookie('merge-insertion-sort', base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode(),
                    secure=True, httponly=False)
    return resp
