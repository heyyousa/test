from django.shortcuts import render,redirect
from worklog_web.models import *
from django.http import HttpResponse
import hashlib

# Create your views here.

def login(request):
    if request.method=="POST":
        userid=request.POST.get('userid')
        userpsw=request.POST.get('userpsw')

        #计算哈希值,暂不使用
        # m=hashlib.md5()
        # m.update(userpsw.encode())
        # userpsw_m=m.hexdigest()

        #异常处理，防止工号错误报错
        try:
            db_userinfo=Userinfo.objects.get(id=userid)
        except Exception as e:
            print('--工号错误 %s'%(e))
            return HttpResponse('工号或密码错误')

        #比对工号和密码正确则登录到mainpage
        if userid==db_userinfo.id and userpsw==db_userinfo.password:
            response=redirect('/worklog_web/mainpage')
            response.set_cookie('userid',userid,3600)
            response.set_cookie('userpsw',userpsw,3600)
            request.session['userid']=userid
            return response
        else:
            return render(request,'login2.html')

    elif request.method=="GET":
        return render(request, 'login2.html')


def signpage(request):
    if request.method=="POST":
        userid = request.POST.get('id')
        username = request.POST.get('name')
        usersex = request.POST.get('sex')
        userpsw = request.POST.get('password')
        pswcfm = request.POST.get('pswcfm')
        userks = request.POST.get('keshi')
        userduty = request.POST.get('duty')

        #判断两次输入的密码是否一致
        if userpsw!=pswcfm:
            return HttpResponse('两次密码不一致')

        #判断工号是否重复，该方式解决不了高并发
        # if Userinfo.objects.filter(id=userid):
        #     return HttpResponse('工号已存在')

        #哈希加密密码，暂不使用
        # m=hashlib.md5()
        # m.update(userpsw.encode())
        # userpsw_m=m.hexdigest()

        #异常处理，写入用户数据，有可能报错，重复插入，try解决并发问题
        try:
            user=Userinfo.objects.create(id=userid,name=username,sex=usersex,password=userpsw,keshi=userks,duty=userduty)
        except Exception as e:
            print('--create user error %s'%(e))
            return HttpResponse('工号已注册')

        #session
        request.session['id']=user.id
        request.session['password']=user.userpsw

        return redirect('/login/')

    elif request.method=="GET":
        return render(request, 'signpage.html')


def testpage(request):
    return render(request,'worklog_web/test.html')