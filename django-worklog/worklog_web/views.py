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
            userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__month=datetime.datetime.now().month) & Q(is_active=True)).order_by('date')
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
        user=Userinfo.objects.get(id=userid)

        if not bool(a):
            lindex = "00000001"
            userwlindex = lindex
        else:
            lindex = int(a.index)
            lindex += 1
            userwlindex = str(lindex).zfill(8)

        userwldate=request.POST.get('date')
        userwlneeds=request.POST.get('needs')
        if userwlneeds=='':
            userwlneeds='否'
        userwlks = request.POST.get('place')
        userwlqsort = request.POST.get('qsort')
        userwlqdsb = request.POST.get('qdescribe')
        userwlfst = request.POST.get('fisstatu')
        userwlnote = request.POST.get('note')

        try:
            Userworklog.objects.create(id=userwlid,index=userwlindex,date=userwldate,needs=userwlneeds,place=userwlks,qsort=userwlqsort,qdescribe=userwlqdsb,fisstatu=userwlfst,note=userwlnote,ct_operator=user.name)
        except Exception as e:
            print ('--index写入重复 %s'%(e))
            return HttpResponse('请重新添加')

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


#查询日志功能
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
        try:
            if place!="":
                if needs!="":
                    if qsort!="":
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(needs=needs) & Q(qsort=qsort) & Q(is_active=True)).order_by('date')
                    else:
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(needs=needs) & Q(is_active=True)).order_by('date')
                else:
                    if qsort!="":
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(qsort=qsort) & Q(is_active=True)).order_by('date')
                    else:
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(place=place) & Q(is_active=True)).order_by('date')
            else:
                if needs!="":
                    if qsort!="":
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(needs=needs) & Q(qsort=qsort) & Q(is_active=True)).order_by('date')
                    else:
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(needs=needs) & Q(is_active=True)).order_by('date')
                else:
                    if qsort!="":
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(qsort=qsort) & Q(is_active=True)).order_by('date')
                    else:
                        userworklogs = Userworklog.objects.filter(Q(id=userid) & Q(date__gte=sdate) & Q(date__lte=fdate) & Q(is_active=True)).order_by('date')
        except Exception as e:
            print('--日期错误 %s'%(e))
            return HttpResponse('日期输入错误')

        return render(request,'worklog_web/logcheckpage.html',locals())

#修改日志，用ajax
# def wl_update(request):
#     if request.method=="GET":
#         wlindex=request.GET.get()


#日志伪删除功能
def wl_delete(request):
    wl_index=request.GET.get('wl_index')
    operator_userid=request.COOKIES.get('userid')
    opuser=Userinfo.objects.get(id=operator_userid)

    if not wl_index:
        return HttpResponse('请求索引有误')

    try:
        wl=Userworklog.objects.get(index=wl_index)
    except Exception as e:
        print('--index有问题 %s'%(e))
        return HttpResponse('index错误')

    if wl.is_active:
        wl.is_active=False
        wl.ud_operator=opuser.name
        wl.save()
    else:
        return HttpResponse('该日志已被删除')

    return HttpResponseRedirect('/worklog_web/logcheckpage')


#超级用户页面
def superuser(request):
    userid=request.COOKIES.get('userid')
    spuser=Userinfo.objects.get(id=userid)
    if spuser.is_spuser:
        users=Userinfo.objects.all()
        return render(request,'worklog_web/superuser.html',locals())
    else:
        return HttpResponse('您不是超级用户不能访问该页面')


#账户禁用功能
def user_disable(request):
    userid=request.GET.get('userid')
    operator_userid=request.COOKIES.get('userid')
    opuser=Userinfo.objects.get(id=operator_userid)

    if not userid:
        return HttpResponse('请求ID异常')

    try:
        user=Userinfo.objects.get(id=userid)
    except Exception as e:
        print('--工号有误 %s'%(e))
        return HttpResponse('id有误')

    if not user.is_spuser:
        if user.is_active:
            user.is_active=False
            user.ud_operator=opuser.name
            user.save()
        else:
            return HttpResponse('该账户已被禁用')
    else:
        return HttpResponse('超级用户不能被操作')

    return HttpResponseRedirect('/worklog_web/superuser')


#账户启用功能
def user_enable(request):
    userid = request.GET.get('userid')
    operator_userid=request.COOKIES.get('userid')
    opuser=Userinfo.objects.get(id=operator_userid)

    if not userid:
        return HttpResponse('请求ID异常')

    try:
        user = Userinfo.objects.get(id=userid)
    except Exception as e:
        print('--工号有误 %s' % (e))
        return HttpResponse('id有误')

    if not user.is_spuser:
        if not user.is_active:
            user.is_active = True
            user.ud_operator=opuser.name
            user.save()
        else:
            return HttpResponse('该用户已启用')
    else:
        return HttpResponse('超级用户不能被操作')

    return HttpResponseRedirect('/worklog_web/superuser')


#机房巡检添加页面
def svlogctpage(request):
    userid=request.COOKIES.get('userid')
    user=Userinfo.objects.get(id=userid)
    svlogs=Serverroomlog.objects.all()
    return render(request,'worklog_web/svlogctpage.html',locals())


#机房巡检添加功能
def add_svlog(request):
    if request.method=="POST":
        userid=request.COOKIES.get('userid')
        user=Userinfo.objects.get(id=userid)

        svlogdate=request.POST.get('date')
        svlogups=request.POST.get('ups')
        svlogservers=request.POST.get('servers')
        svlogac=request.POST.get('air_conditioner')
        svlogtp=request.POST.get('temperature')
        svloghd=request.POST.get('humidity')
        svlognote=request.POST.get('note')

        a=Serverroomlog.objects.last()
        if not bool(a):
            slindex = "00000001"
            svlogindex = slindex
        else:
            slindex = int(a.index)
            slindex += 1
            svlogindex = str(slindex).zfill(8)

        try:
            Serverroomlog.objects.create(id=userid,index=svlogindex,date=svlogdate,ups=svlogups,servers=svlogservers,air_conditioner=svlogac,temperature=svlogtp,humidity=svloghd,note=svlognote,creater=user.name)
        except Exception as e:
            print('--index重复插入 %s'%(e))
            return HttpResponse('请重新添加')

        return HttpResponseRedirect('/worklog_web/svlogctpage')


def test(request):
    userid='001'
    userworklogs = Userworklog.objects.filter(id=userid)
    user = Userinfo.objects.filter(id=userid)
    return HttpResponse(locals())