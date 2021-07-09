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


admin.site.register(Userinfo,UserinfoManager)
admin.site.register(Userworklog,UserworklogManager)