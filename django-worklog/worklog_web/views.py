from django.shortcuts import render
from worklog_web.models import *
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

def mainpage(request):
    userworklogs = Userworklog.objects.all()
    if request.method=="POST":
        if request.POST.get('needs')=="是":
            userwlneeds =1
        else:
            userwlneeds =0
        userwlid="001"
        a=Userworklog.objects.last()
        lindex=int(a.index)
        lindex+=1
        userwlindex=str(lindex).zfill(8)
        userwldate=request.POST.get('date')
        userwlks = request.POST.get('place')
        userwlqsort = request.POST.get('qsort')
        userwlqdsb = request.POST.get('qdescribe')
        userwlfst = request.POST.get('fisstatu')
        userwlnote = request.POST.get('note')
        Userworklog.objects.create(id=userwlid,index=userwlindex,date=userwldate,needs=userwlneeds,place=userwlks,qsort=userwlqsort,qdescribe=userwlqdsb,fisstatu=userwlfst,note=userwlnote)
        return redirect('/worklog_web/mainpage')
    elif request.method=="GET":
        return render(request, 'worklog_web/mainpage.html', locals())


def all_user(request):
    all_user=Userinfo.objects.all()
    return render(request,'worklog_web/all_user.html',locals())

def testvalues(request):
    userid=Userinfo.objects.filter(id__exact='001')
    return render(request,'worklog_web/test.html',locals())