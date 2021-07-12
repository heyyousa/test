from django.contrib import admin
from .models import *

# Register your models here.

# admin表单展示优化
class UserinfoManager(admin.ModelAdmin):
    list_display = ['id','name','sex','keshi','duty']
    search_fields = ['id','name','sex','keshi','duty']

class UserworklogManager(admin.ModelAdmin):
    list_display = ['id','date','needs','place','qsort','qdescribe','fisstatu','note']
    search_fields = ['id','date','place','qsort','fisstatu']
    list_filter = ['id']

class ServerroomlogManager(admin.ModelAdmin):
    list_display = ['id', 'date', 'ups', 'servers', 'systime', 'air_conditioner', 'temperature', 'humidity','note','creater','is_active','ud_operator']
    search_fields = ['id', 'date', 'ups', 'servers', 'systime', 'air_conditioner', 'temperature', 'humidity','note','creater','is_active','ud_operator']

admin.site.register(Userinfo,UserinfoManager)
admin.site.register(Userworklog,UserworklogManager)
admin.site.register(Serverroomlog,ServerroomlogManager)