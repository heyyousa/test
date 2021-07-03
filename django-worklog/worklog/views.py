from django.shortcuts import render,redirect
from worklog_web.models import *
from django.http import HttpResponse

# Create your views here.

def login(request):
    if request.method=="POST":
        userid=request.POST.get('userid')
        userpsw=request.POST.get('userpsw')
        db_userinfo=Userinfo.objects.get(id=userid)
        if userid==db_userinfo.id and userpsw==db_userinfo.password:
            response=redirect('/worklog_web/mainpage')
            response.set_cookie('userid',userid,3600)
            response.set_cookie('userpsw',userpsw,3600)
            return response
        else:
            return render(request,'login2.html')
    elif request.method=="GET":
        return render(request, 'login2.html')


def signpage(request):
    return render(request, 'signpage.html')


def signup(request):
    if request.method=="POST":
        userid = request.POST.get('id')
        username = request.POST.get('name')
        usersex = request.POST.get('sex')
        userpsw = request.POST.get('password')
        userks = request.POST.get('keshi')
        userduty = request.POST.get('duty')
        Userinfo.objects.create(id=userid,name=username,sex=usersex,password=userpsw,keshi=userks,duty=userduty)
        return render(request,'login2.html')
    else:
        pass


def testpage(request):
    return render(request,'worklog_web/test.html')