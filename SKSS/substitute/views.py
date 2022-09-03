from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.db.models import Q

# Create your views here.
from .models import Course, ClassLeader, Condition, SubstituteAsk, Entry
from .forms import LoginForm, InitializeForm

import datetime
now = datetime.datetime.now()

def login_checker(func):
    def checker(request, **kwargs):
        if 'cl_id' not in request.session:
            return HttpResponseRedirect(reverse('substitute:login'))
        else:
            return func(request, **kwargs)
    return checker

def is_email(_string):
    return '@' in _string

def find_cl_by_email(_email):
    cl = ClassLeader.objects.filter(email=_email)
    return cl

def find_cl_by_staffID(_staffID):
    cl = ClassLeader.objects.filter(staffID=_staffID)
    return cl

@login_checker
def index(request):
    return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identification = form.cleaned_data['identification']
            password = form.cleaned_data['password']
            if is_email(identification):
                matched_cls = find_cl_by_email(identification)
            else:
                matched_cls = find_cl_by_staffID(identification)

            # ユーザ名の確認
            if len(matched_cls) == 0:
                messages.error(request, '職員IDもしくはメールアドレスが正しくありません')
            else:
                cl = matched_cls[0]
                is_auth = check_password(password, cl.password)

                # パスワードの確認
                if is_auth:
                    request.session['cl_id'] = cl.id
                    # 初期パスワードの場合に変更を強制
                    if password == '0000':
                        return HttpResponseRedirect(reverse('substitute:initialize'))
                    else:
                        messages.success(request, f'お疲れ様です、{cl.name}様')
                        return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))
                else:
                    messages.error(request, 'パスワードが正しくありません')         

    return render(request, 'substitute/login.html', {
        'form': LoginForm()
    })
    return 0

@login_checker
def initialize(request):
    message = ""
    cl = ClassLeader.objects.get(id=request.session['cl_id'])

    if request.method == 'POST':
        form = InitializeForm(request.POST)
        if form.is_valid():
            input_password1 = form.cleaned_data['password1']
            input_password2 = form.cleaned_data['password2']

            # 2回入力のパスワードが合っているかの確認
            if input_password1 == input_password2:
                # 変更なしを許さない
                if input_password1 == '0000':
                    message = 'パスワードを変更してください'
                else:
                    cl.password = make_password(input_password1)
                    cl.save()
                return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))
            else:
                message = 'パスワードが一致していません'

    return render(request, 'substitute/initialize.html', {
        'message': message, 
        'form': InitializeForm()
    })

@login_checker
def home(request, year, month):
    from . import mixins
    cl = ClassLeader.objects.get(id=request.session['cl_id'])

    # カレンダー表示に使う情報
    calendar = mixins.MonthCalendarMixin()
    calendar_data = calendar.get_month_calendar(year, month)
    month_days_asks = []
    for week in calendar_data['month_days']:
        week_days_asks = []
        # ある日の代行依頼を取得, 日付とセットで保存してhtmlに渡す
        for day in week:
            day_asks = SubstituteAsk.objects.filter(date=day)
            day_days_asks = {'day': day, 'asks': day_asks}
            week_days_asks.append(day_days_asks)
        month_days_asks.append(week_days_asks)
    
    # テーブル表示に使う情報
    asks_after_now = SubstituteAsk.objects.filter(date__gte=now).order_by('date')

    return render(request, 'substitute/home.html', {
        'calendar_data': calendar_data, 
        'month_days_asks': month_days_asks, 
        'asks_after_now': asks_after_now, 
        'cl': cl
    })

@login_checker
def specification(request, ask_id):
    return 0

@login_checker
def revise(request, ask_id):
    return 0

@login_checker
def make(request):
    return 0

@login_checker
def confirmAsk(request):
    return 0

@login_checker
def confirmEntry(request):
    return 0

@login_checker
def logout(request):
    return 0