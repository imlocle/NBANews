from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^nba_news$', views.nba_news),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout)
]