from django.urls import path
from . import views

app_name = "oauth"
urlpatterns = [
    path('', views.oauth_index, name='oauth_index'),
    path('callback', views.oauth_callback, name='oauth_callback'),
]
