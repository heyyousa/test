from django.shortcuts import render,redirect
from worklog_web.models import *
from django.http import HttpResponse,HttpResponseRedirect
import hashlib

# Create your views here.

#登录
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
            message='工号或密码错误'
            return render(request,'messagepage.html',locals())

        if not db_userinfo.is_active:
            message='工号被禁用'
            return render(request,'messagepage.html',locals())

        #比对工号和密码正确则登录到mainpage
        if userid==db_userinfo.id and userpsw==db_userinfo.password:
            user=Userinfo.objects.get(id=userid)
            resp=redirect('/worklog_web/mainpage')
            resp.set_cookie('userid',userid,60*60*2)
            resp.set_cookie('userpsw',user.password,2)
            return resp
        else:
            message='账号或密码有误'
            return render(request,'messagepage.html',locals())

    elif request.method=="GET":
        #检查session登陆状态,本项目不适用保存登录状态
        # if request.session.get('userid') and request.session.get('userpsw'):
        #     return redirect('/worklog_web/mainpage')

        #检查cookie
        # c_userid=request.COOKIES.get('userid')
        # c_userpsw=request.COOKIES.get('userpsw')
        #
        # if c_userid and c_userpsw:
        #     request.session['userid']=c_userid
        #     return  redirect('/worklog_web/mainpage')

        return render(request, 'login2.html')

#注册页面包含注册功能
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
            message='两次密码不一致'
            return render(request,'messagepage.html',locals())

        if username=='' or usersex=='' or userpsw=='' or pswcfm=='' or userks=='' or userduty=='':
            message='所填信息不能为空'
            return render(request,'messagepage.html',locals())

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
            message='工号已注册'
            return render(request,'messagepage.html',locals())

        #存储session
        # request.session['id']=user.id
        # request.session['password']=user.userpsw

        return redirect('/login/')

    elif request.method=="GET":
        return render(request, 'signpage.html')


def testpage(request):
    return render(request,'worklog_web/test.html')