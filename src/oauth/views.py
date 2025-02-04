# authapp/views.py
import datetime
import jwt
import requests
from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def oauth_index(request):
  # TODO: check user has already authenticated
  base_url = 'https://api.intra.42.fr/oauth/authorize'
  query_params = {
    'client_id':settings.OAUTH_UID,
    'redirect_uri': f"https://{request.get_host()}{reverse('oauth:oauth_callback')}",
    'response_type': 'code'
  }
  return redirect(f'{base_url}?{urlencode(query_params)}')

@csrf_exempt
def oauth_callback(request):
  resp = requests.post(
    url = 'https://api.intra.42.fr/oauth/token',
    data = {
      'code': request.GET['code'],
      'client_id': settings.OAUTH_UID,
      'client_secret': settings.OAUTH_SECRET,
      'grant_type': 'authorization_code',
      'redirect_uri': f"https://{request.get_host()}{request.path}"
    }
  )

  # TODO: fetch user info from 42 server
  user_info = {
      'id': 1,
      'username': 'testuser',
      'email': 'testuser@example.com',
  }

  # TODO: save user info and jwt key to database
  payload = {
      'user_id': user_info['id'],
      'username': user_info['username'],
      'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)
  }
  token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
  return JsonResponse({'token': token, 'user': user_info, 'raw': resp.text})
