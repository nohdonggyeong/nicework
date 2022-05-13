from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from common.models import MyUser
from leave.models import LevHistory
from ..models import CmtHistory
from django.core.paginator import Paginator
import datetime


@login_required(login_url='common:login')
def history(request):
    # 로그인한 계정의 출퇴근 내역 가져오기
    myuser = get_object_or_404(MyUser, email=request.user.email)
    mylist = CmtHistory.objects.filter(employee=myuser).order_by('-startdatetime')

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'mylist': page_obj}
    return render(request, 'commute/commute_hist.html', context)


@login_required(login_url='common:login')
def situation(request):
    today = datetime.date.today()
    today_start = datetime.datetime.combine(today, datetime.time(0, 0, 0))
    today_end = datetime.datetime.combine(today, datetime.time(23, 59 ,59))
    commuters = CmtHistory.objects.filter(startdatetime__gte=today_start, startdatetime__lte=today_end).order_by('startdatetime', 'enddatetime')
    commuting_list = []
    for i in commuters:
        commuting_list.append(i.employee.realname)

    noncommute_users = MyUser.objects.filter().exclude(realname__in=commuting_list).order_by('realname')
    today_leave_list = LevHistory.objects.filter(startdate__lte=today, enddate__gte=today, is_approved=True).order_by('startdate')
    leave_dict = {'AL':'연차', 'MO':'오전 반차', 'AO':'오후 반차', 'CV':'경조 휴가', 'OL':'공가', 'EL':'조퇴', 'AB':'결근', 'SL':'병가'}
    noncommuters = []
    for i in noncommute_users:
        todaycat = '-'
        for j in today_leave_list:
            if str(j.employee_id) == str(i.id):
                todaycat = leave_dict.get(str(j.leavecat))
        noncommuters.append({'realname':i.realname, 'todaycat':todaycat, 'openingtime':i.openingtime})
     
    context = {'commuters': commuters, 'noncommuters': noncommuters}
    return render(request, 'commute/commute_situ.html', context)


@login_required(login_url='common:login')
def totalhistory(request):
    # 전체 출근내역 가져오기
    mylist = CmtHistory.objects.filter().order_by('-startdatetime')

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'mylist': page_obj}
    return render(request, 'commute/commute_toth.html', context)