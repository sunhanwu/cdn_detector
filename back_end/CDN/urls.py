from django.urls import path

from . import views

urlpatterns = [
    path('', views.listorders),
    path('neo4j', views.listneo4j),
]