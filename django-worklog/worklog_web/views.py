from django.shortcuts import render,redirect
from worklog_web.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from django.utils.http import urlquote
import datetime
import pandas as pd
import xlwt
import xlrd

# Create your views here.

#检查登录状态装饰器
def checklogin(fn):
    def wrap(request,*args,**kwargs):
        userid=request.COOKIES.get('userid')
        if not userid:
            return HttpResponseRedirect('/login')

        return fn(request,*args,**kwargs)
    return wrap


#调取用户信息的函数,返回user实例
def uinfo(request):
    userid=request.COOKIES.get('userid')
    user=Userinfo.objects.get(id=userid)
    return user


#响应主页GET
@checklogin
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
            resp=redirect('/login')
            return resp


#新建日志，响应主页POST
@checklogin
def create_log(request):
    if request.method=="POST":
        user=uinfo(request)
        userwlid=user.id
        a=Userworklog.objects.last()

        if not bool(a):
            lindex = "00000001"
            userwlindex = lindex
        else:
            lindex = int(a.index)
            lindex += 1
            userwlindex = str(lindex).zfill(8)

        userwldate=request.POST.get('date')
        if userwldate=='':
            userwldate=datetime.date.today()

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
            message = '请重新添加'
            return render(request, 'worklog_web/messagepage.html', locals())

        return redirect('/worklog_web/mainpage')
        #render(request,'worklog_web/mainpage.html',locals())


#注销登录
def logout(request):
    resp=HttpResponseRedirect('/login')
    resp.delete_cookie('userid')
    resp.delete_cookie('userpsw')
    return resp


#查询页面响应get
@checklogin
def logcheckpage(request):
    if request.method=="GET":
        user=uinfo(request)
        return render(request,'worklog_web/logcheckpage.html',locals())


#查询日志功能
@checklogin
def logcheck(request):
    if request.method=="POST":
        user=uinfo(request)
        userid=user.id

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
            message = '日期输入错误'
            return render(request, 'worklog_web/messagepage.html', locals())


        return render(request,'worklog_web/logcheckpage.html',locals())


#修改日志，用ajax
# def wl_update(request):
#     if request.method=="GET":
#         wlindex=request.GET.get()


#日志伪删除功能
@checklogin
def wl_delete(request):
    wl_index=request.GET.get('wl_index')
    opuser=uinfo(request)

    if not wl_index:
        message = '请求索引异常'
        return render(request, 'worklog_web/messagepage.html', locals())

    try:
        wl=Userworklog.objects.get(index=wl_index)
    except Exception as e:
        print('--index有问题 %s'%(e))
        message = '请重新添加'
        return render(request, 'worklog_web/messagepage.html', locals())

    if wl.is_active:
        wl.is_active=False
        wl.ud_operator=opuser.name
        wl.save()
    else:
        message = '该日志已被删除'
        return render(request, 'worklog_web/messagepage.html', locals())

    return HttpResponseRedirect('/worklog_web/logcheckpage')


#超级用户页面
@checklogin
def superuser(request):
    spuser=uinfo(request)
    if spuser.is_spuser:
        users=Userinfo.objects.all()
        return render(request,'worklog_web/superuser.html',locals())
    else:
        message = '非超级用户不能访问该页面'
        return render(request, 'worklog_web/messagepage.html', locals())


#查询用户功能
@checklogin
def usercheck(request):
    if request.method=="POST":
        spuser=uinfo(request)

        userid=request.POST.get('id')
        username=request.POST.get('name')
        userkeshi=request.POST.get('keshi')
        userduty=request.POST.get('duty')
        useractive=request.POST.get('is_active')

        q=Q()
        if userid!='':
            q &= Q(id=userid)
        if username!='':
            q &=Q(name=username)
        if userkeshi!='':
            q &= Q(keshi=userkeshi)
        if userduty!='':
            q &= Q(duty=userduty)
        if useractive!='':
            q &= Q(is_active=useractive)

        users=Userinfo.objects.filter(q)

        return render(request,'worklog_web/superuser.html',locals())


#账户禁用功能
@checklogin
def user_disable(request):
    userid=request.GET.get('userid')
    operator_user=uinfo(request)
    operator_userid=operator_user.id
    opuser=Userinfo.objects.get(id=operator_userid)

    if not userid:
        message = '请求ID异常'
        return render(request, 'worklog_web/messagepage.html', locals())

    try:
        user=Userinfo.objects.get(id=userid)
    except Exception as e:
        print('--工号有误 %s'%(e))
        message = '工号异常'
        return render(request, 'worklog_web/messagepage.html', locals())

    if not user.is_spuser:
        if user.is_active:
            user.is_active=False
            user.ud_operator=opuser.name
            user.save()
        else:
            message = '该账户已被禁用'
            return render(request, 'worklog_web/messagepage.html', locals())
    else:
        message = '超级用户不能被操作'
        return render(request, 'worklog_web/messagepage.html', locals())

    return HttpResponseRedirect('/worklog_web/superuser')


#账户启用功能
@checklogin
def user_enable(request):
    userid = request.GET.get('userid')
    operator_user=uinfo(request)
    operator_userid=operator_user.id
    opuser=Userinfo.objects.get(id=operator_userid)

    if not userid:
        message='请求ID异常'
        return render(request,'worklog_web/messagepage.html',locals())

    try:
        user = Userinfo.objects.get(id=userid)
    except Exception as e:
        print('--工号有误 %s' % (e))
        message = 'ID有误'
        return render(request, 'worklog_web/messagepage.html', locals())

    if not user.is_spuser:
        if not user.is_active:
            user.is_active = True
            user.ud_operator=opuser.name
            user.save()
        else:
            message = '用户已启用'
            return render(request, 'worklog_web/messagepage.html', locals())
    else:
        message = '超级用户不能被操作'
        return render(request, 'worklog_web/messagepage.html', locals())

    return HttpResponseRedirect('/worklog_web/superuser')


#机房巡检页面
@checklogin
def svlogctpage(request):
    user=uinfo(request)
    svlogs=Serverroomlog.objects.filter(Q(is_active=True))
    return render(request,'worklog_web/svlogctpage.html',locals())


#机房巡检添加功能
@checklogin
def add_svlog(request):
    if request.method=="POST":
        user=uinfo(request)

        svlogdate=request.POST.get('date')
        svlogups=request.POST.get('ups')
        svlogservers=request.POST.get('servers')
        svlogsystime=request.POST.get('systime')
        svlogac=request.POST.get('air_conditioner')
        svlogtp=request.POST.get('temperature')
        svloghd=request.POST.get('humidity')
        svlognote=request.POST.get('note')

        if not svlogups:
            svlogups='正常'
        if not svlogservers:
            svlogservers='正常'
        if not svlogsystime:
            svlogsystime='正常'
        if not svlogac:
            svlogac='正常'

        if not svlogtp or not svloghd or not svlogdate:
            message='请输入日期、温度、湿度'
            return render(request,'worklog_web/messagepage.html',locals())

        a=Serverroomlog.objects.last()
        if not bool(a):
            slindex = "00000001"
            svlogindex = slindex
        else:
            slindex = int(a.index)
            slindex += 1
            svlogindex = str(slindex).zfill(8)

        try:
            Serverroomlog.objects.create(id=user.id,index=svlogindex,date=svlogdate,ups=svlogups,servers=svlogservers,systime=svlogsystime,air_conditioner=svlogac,temperature=svlogtp,humidity=svloghd,note=svlognote,creater=user.name)
        except Exception as e:
            print('--index重复插入 %s'%(e))
            message='请重新添加'
            return render(request,'worklog_web/messagepage.html',locals())

        return HttpResponseRedirect('/worklog_web/svlogctpage')


#全部日志页面
@checklogin
def alllogpage(request):
    spuser=uinfo(request)
    return render(request,'worklog_web/alllogpage.html',locals())


#全部日志查询功能
@checklogin
def alllog_check(request):
    if request.method=="POST":
        spuser=uinfo(request)

        uid=request.POST.get('id')
        if uid!='':
            user=Userinfo.objects.get(id=uid)

        sdate=request.POST.get('sdate')
        fdate=request.POST.get('fdate')
        place=request.POST.get('place')
        needs=request.POST.get('needs')
        qsort=request.POST.get('qsort')

        if sdate=='':
            sdate=datetime.datetime.now()
        if fdate=='':
            fdate=datetime.datetime.now()

        q=Q()
        q &= Q(is_active=True)

        if place != '':
            q &= Q(place=place)
        if needs != '':
            q &= Q(needs=needs)
        if qsort != '':
            q &= Q(qsort=qsort)
        if sdate != '':
            q &= Q(date__gte=sdate)
        if fdate != '':
            q &= Q(date__lte=fdate)
        if uid!='':
            q &= Q(id=uid)

        alllogs=Userworklog.objects.filter(q).order_by('date')

        print(q,alllogs,spuser)
        return render(request,'worklog_web/alllogpage.html',locals())


#当月日志导出excel功能
@checklogin
def wlexcel(request):
    user=uinfo(request)

    resp=HttpResponse(content_type='application/ms-excel')
    filename='工作日志.xls'
    filename=urlquote(filename)
    resp['Content-Disposition']='attachment; filename=%s'%(filename)

    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('sheet1')
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    # 不同数据表列名不同
    cols=['日期','系统需求','问题科室','问题类型','问题简述','处理结果','备注']
    frow=0

    logs=Userworklog.objects.filter(Q(id=user.id) & Q(date__month=datetime.datetime.now().month) & Q(is_active=True)).values_list('date','needs','place','qsort','qdescribe','fisstatu','note')

    for col in range(len(cols)):
        ws.write(frow,col,cols[col],font_style)

    font_style = xlwt.XFStyle()

    for row in range(len(logs)):
        row+=1
        print(len(logs))
        for col in range(len(cols)):
            ws.write(row,col,logs[row-1][col],font_style)

    wb.save(resp)
    return resp


#值班表
@checklogin
def zhiban(request):
    zb=pd.read_excel('worklog_web/zhiban/zhiban.xls')
    zb_html=zb.to_html()
    return render(request,'worklog_web/zhibanpage.html',locals())



def test(request):
    user=uinfo(request)
    q=Q()
    uname=''
    uid='002'
    usex='男'
    if uname!='':
        q &= Q(name=uname)
    if uid!='':
        q &= Q(id=uid)
    if usex!='':
        q &= Q(sex=usex)
    print(q)
    users=Userinfo.objects.filter(q)
    print(users)
    return render(request,'worklog_web/test.html',locals())