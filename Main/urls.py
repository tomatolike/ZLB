from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from . import views
urlpatterns = [
    url(r'^login/', views.login),
    url(r'^register/',views.register),
    url(r'^logIn/',views.logIn),
]

urlpatterns += staticfiles_urlpatterns()