from django.contrib import admin
from django.urls import path
from worklog_web import views


urlpatterns = [
    path('mainpage/', views.mainpage),
    path('create_log/',views.create_log),
    path('logout/',views.logout),
    path('logcheck/',views.logcheck),
    path('logcheckpage/',views.logcheckpage),
    #path('wl_update/',views.wl_update),
    path('wl_delete/',views.wl_delete),
    path('superuser/',views.superuser),
    path('user_disable/',views.user_disable),
    path('user_enable/',views.user_enable),
    path('svlogctpage/',views.svlogctpage),
    path('add_svlog/',views.add_svlog),

]