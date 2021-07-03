from django.contrib import admin
from django.urls import path
from worklog_web import views


urlpatterns = [
    path('mainpage/', views.mainpage),
    path('create_log/',views.create_log),
]