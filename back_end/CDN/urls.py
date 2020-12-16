"""
Author: Sun Peishuai
Date: 2020-12-08
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.listorders),
    path('neo4j', views.listneo4j),
]