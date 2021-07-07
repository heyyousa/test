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
    user=Userinfo.objects.get(id=userid)

    # 响应GET请求
    if request.method=="GET":
        # 借用2秒存活时间的cookie防止用户直接进入mainpage
        if request.COOKIES.get('userid'):
            return render(request, 'worklog_web/mainpage.html', locals())
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
        return redirect('/worklog_web/mainpage')
        #render(request,'worklog_web/mainpage.html',locals())


def logout(request):
    request.delete_cookie('userid')
    request.delete_cookie('userpsw')
def test(request):
    userid='001'
    userworklogs = Userworklog.objects.filter(id=userid)
    user = Userinfo.objects.filter(id=userid)
    return HttpResponse(locals())