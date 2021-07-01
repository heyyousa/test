from django.contrib import admin
from django.urls import path
from worklog_web import views


urlpatterns = [
    path('mainpage/', views.mainpage),
    path('all_user/',views.all_user),
    path('testvalues',views.testvalues)
]