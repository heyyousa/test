from django.shortcuts import render,redirect
from worklog_web.models import *
from django.http import HttpResponse
from django.db.models import Q
import datetime

# Create your views here.

def mainpage(request):
    # 从cookie中获取用户ID
    userid=request.COOKIES.get('userid')
    # 查与用户ID一致且当月的工作日志,且按日期升序排序
    userworklogs = Userworklog.objects.filter(Q(id=userid)&Q(date__month=datetime.datetime.now().month)).order_by('date')
    # 获取该ID的用户信息
    if request.COOKIES.get('userid'):
        user=Userinfo.objects.get(id=userid)
    else:
        pass

    # 响应GET请求
    if request.method=="GET":
        # 判断用户是否登录
        if request.COOKIES.get('userid'):
            if request.COOKIES.get('userpsw')==user.password and request.COOKIES.get('userid')==user.id:
                return render(request, 'worklog_web/mainpage.html', locals())
            else:
                resp = redirect('/login/')
                return resp
        else:
            resp=redirect('/login/')
            return resp


def create_log(request):
    userid = request.COOKIES.get('userid')
    user = Userinfo.objects.get(id=userid)
    if request.method=="POST":
        userwlid=userid
        a=Userworklog.objects.last()
        lindex=int(a.index)
        lindex+=1
        userwlindex=str(lindex).zfill(8)
        userwldate=request.POST.get('date')
        userwlneeds=request.POST.get('needs')
        if userwlneeds=='':
            userwlneeds='否'
        userwlks = request.POST.get('place')
        userwlqsort = request.POST.get('qsort')
        userwlqdsb = request.POST.get('qdescribe')
        userwlfst = request.POST.get('fisstatu')
        userwlnote = request.POST.get('note')
        Userworklog.objects.create(id=userwlid,index=userwlindex,date=userwldate,needs=userwlneeds,place=userwlks,qsort=userwlqsort,qdescribe=userwlqdsb,fisstatu=userwlfst,note=userwlnote)
        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__month=datetime.datetime.now().month)).order_by('date')
        return render(request,'worklog_web/mainpage.html',locals())


def test(request):
    userid='001'
    userworklogs = Userworklog.objects.filter(id=userid)
    user = Userinfo.objects.filter(id=userid)
    return HttpResponse(locals())