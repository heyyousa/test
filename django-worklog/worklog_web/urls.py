from django.contrib import admin
from django.urls import path
from worklog_web import views


urlpatterns = [
    path('mainpage/', views.mainpage),  # 主页
    path('create_log/',views.create_log),  # 添加日志功能
    path('logout/',views.logout),  # 注销功能
    path('logcheck/',views.logcheck),  # 日志查询功能
    path('logcheckpage/',views.logcheckpage),  # 日志查询页面
    #path('wl_update/',views.wl_update),
    path('wl_delete/',views.wl_delete),  # 日志删除功能
    path('superuser/',views.superuser),  # 超级用户页面
    path('usercheck/',views.usercheck),  # 用户查询功能
    path('user_disable/',views.user_disable),  # 用户禁用功能
    path('user_enable/',views.user_enable),  # 用户启用功能
    path('svlogctpage/',views.svlogctpage),  # 机房巡检页面
    path('add_svlog/',views.add_svlog),  # 机房巡检添加功能
    path('alllogpage/',views.alllogpage),  # 全部日志页面
    path('alllog_check/',views.alllog_check),  # 全部日志查询功能
    path('wlexcel/',views.wlexcel),  # 数据表导出excel
    path('zhiban/',views.zhiban),  # 值班表


    path('test/',views.test),  # 测试函数

]