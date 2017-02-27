from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.create_user),
    url(r'^success$', views.success),
    url(r'^home$', views.home),
    url(r'^sessions$', views.login_user),
    url(r'^quote/(?P<user_id>\d+)$', views.quote),
    url(r'^add/(?P<quote_id>\d+)$', views.add),
    url(r'^remove/(?P<favorite_id>\d+)$', views.remove),
    url(r'^user/(?P<user_id>\d+)$', views.user),
]
