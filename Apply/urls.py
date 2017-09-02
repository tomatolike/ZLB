from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from . import views
urlpatterns = [
    url(r'^myinfo/', views.myinfo1),
    url(r'^modifyinfo/', views.modifyinfo),
    url(r'^modifycode/', views.modifycode),
    url(r'^myrecord/', views.myrecord),
    url(r'^infoquery/', views.infoquery),
    url(r'^QCquery/', views.QCquery),
    url(r'^HYSquery/', views.HYSquery),
    url(r'^XB1query', views.XB1query),
    url(r'^XB2query', views.XB2query),
]

urlpatterns += staticfiles_urlpatterns()