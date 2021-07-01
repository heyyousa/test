from django.shortcuts import render
from worklog_web.models import *

# Create your views here.

def login(request):
    if request.method=="POST":
        userid=request.POST.get('userid')
        userpsw=request.POST.get('userpsw')
        next_url=request.POST.get('next_url')
        db_userinfo=Userinfo.objects.get(id=userid)
        if userid==db_userinfo.id and userpsw==db_userinfo.password:
            return render(request,'worklog_web/mainpage.html')
    else:
        return render(request, 'login2.html')

def signpage(request):
    return render(request, 'signpage.html')

def signup(request):

    if request.method=="POST":
        userid = request.POST.get('id')
        username = request.POST.get('name')
        usersex = int(request.POST.get('sex'))
        userpsw = request.POST.get('password')
        userks = request.POST.get('keshi')
        userduty = request.POST.get('duty')
        Userinfo.objects.create(id=userid,name=username,sex=usersex,password=userpsw,keshi=userks,duty=userduty)
    else:
        pass

    return render(request,'signup.html',locals())


def testpage(request):
    return render(request,'worklog_web/test.html')