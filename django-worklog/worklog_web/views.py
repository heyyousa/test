from django.shortcuts import render,redirect
from worklog_web.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
import datetime

# Create your views here.

#响应主页GET
def mainpage(request):
    # 响应GET请求
    if request.method=="GET":
        # 借用2秒存活时间的cookie防止用户直接进入mainpage
        if request.COOKIES.get('userid'):
            # 从cookie中获取用户ID
            userid = request.COOKIES.get('userid')
            # 查与用户ID一致且当月的工作日志,且按日期升序排序
            userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__month=datetime.datetime.now().month)).order_by('date')
            # 获取该ID的用户信息
            user = Userinfo.objects.get(id=userid)
            return render(request, 'worklog_web/mainpage.html', locals())

        else:
            resp=redirect('/login/')
            return resp

#新建日志，响应主页POST
def create_log(request):
    if request.method=="POST":
        userid = request.COOKIES.get('userid')
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

        return redirect('/worklog_web/mainpage')
        #render(request,'worklog_web/mainpage.html',locals())

#注销登录
def logout(request):
    resp=HttpResponseRedirect('/login')
    resp.delete_cookie('userid')
    resp.delete_cookie('userpsw')
    return resp

#查询页面响应get
def logcheckpage(request):
    if request.method=="GET":
        userid=request.COOKIES.get('userid')
        user=Userinfo.objects.get(id=userid)
        return render(request,'worklog_web/logcheckpage.html',locals())

#查询日志
def logcheck(request):
    if request.method=="POST":
        userid=request.COOKIES.get('userid')
        user=Userinfo.objects.get(id=userid)

        place=request.POST.get('place')
        needs=request.POST.get('needs')
        qsort=request.POST.get('qsort')

        if request.POST.get('sdate')=='':
            sdate=datetime.datetime.now()
        else:
            sdate=request.POST.get('sdate')

        if request.POST.get('fdate')=='':
            fdate=datetime.datetime.now()
        else:
            fdate=request.POST.get('fdate')

        #不定查询条件过滤器
        if place!="":
            if needs!="":
                if qsort!="":
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(needs=needs) & Q(qsort=qsort)).order_by('date')
                else:
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(needs=needs)).order_by('date')
            else:
                if qsort!="":
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(qsort=qsort)).order_by('date')
                else:
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place)).order_by('date')
        else:
            if needs!="":
                if qsort!="":
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(needs=needs) & Q(qsort=qsort)).order_by('date')
                else:
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(needs=needs)).order_by('date')
            else:
                if qsort!="":
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(qsort=qsort)).order_by('date')
                else:
                    userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate)).order_by('date')

        return render(request,'worklog_web/logcheckpage.html',locals())


def test(request):
    userid='001'
    userworklogs = Userworklog.objects.filter(id=userid)
    user = Userinfo.objects.filter(id=userid)
    return HttpResponse(locals())