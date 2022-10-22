from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
import json

# Create your views here.
from .models import Grade, Day, Level, Subject, Condition, Course, ClassLeader, SubstituteAsk, Entry
from .forms import LoginForm, InitializeForm, MakeForm, ReviseForm

import datetime
japanese_days = ['月', '火', '水', '木', '金', '土', '日']

def login_checker(func):
    def checker(request, **kwargs):
        if 'cl_id' not in request.session:
            return HttpResponseRedirect(reverse('substitute:login'))
        else:
            return func(request, **kwargs)
    return checker

def get_is_email(_string):
    return '@' in _string

def find_cl_by_email(_email):
    cl = ClassLeader.objects.filter(email=_email)
    return cl

def find_cl_by_staffID(_staffID):
    cl = ClassLeader.objects.filter(staffID=_staffID)
    return cl

def get_is_qualified(_conditions, _qualifications):
    is_ok = 1
    for condition in _conditions:
        if condition not in _qualifications:
            is_ok = 0
    return is_ok


@login_checker
def index(request):
    now = datetime.datetime.now()
    return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))

def login(request):
    now = datetime.datetime.now()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identification = form.cleaned_data['identification']
            password = form.cleaned_data['password']
            if get_is_email(identification):
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

@login_checker
def initialize(request):
    now = datetime.datetime.now()
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
    now = datetime.datetime.now()

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
        'cl': cl, 
        'calendar_data': calendar_data, 
        'month_days_asks': month_days_asks, 
        'asks_after_now': asks_after_now
        })

# 過去のものはデータ数がエグくなるから別ページに
@login_checker
def past(request):
    now = datetime.datetime.now()
    asks_past = SubstituteAsk.objects.filter(date__lt=now).order_by('date').reverse()

    return render(request, 'substitute/past.html', {
        'asks_past': asks_past
    })

@login_checker
def specification(request, ask_id):
    now = datetime.datetime.now()
    cl = ClassLeader.objects.get(id=request.session['cl_id'])
    ask = SubstituteAsk.objects.get(id=ask_id)
    assumed_courses = ask.client.courses.filter(day=ask.day)

    if request.method == 'POST':
        # 応募が送信された場合の処理
        if 'entrant' in request.POST.dict().keys():
            entry = Entry(
            date=now, 
            day=Day.objects.get(name=japanese_days[now.weekday()]), 
            state='応募中', 
            cl=cl, 
            ask=ask)
            entry.save()

            # 応募できた時の応募者への通知
            mail_subject = '代行への応募完了の通知'
            mail_context = {
                'cl': cl, 
                'ask': ask, 
                'assumed_courses': assumed_courses
            }
            mail_message_html = render_to_string('substitute/mails/entry_notice.html', mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_bcc_list = [cl.email]
            mail = EmailMessage(
                subject=mail_subject, 
                body=mail_message, 
                from_email = settings.DEFAULT_FROM_EMAIL, 
                to=[settings.DEFAULT_FROM_EMAIL], 
                bcc=mail_bcc_list
                )
            mail.send()

            # 新しい応募があった時の依頼者への通知
            mail_subject = '新規応募の通知'
            mail_context = {
                'cl': cl, 
                'ask': ask, 
                'entry_num': len(ask.entries.all())
            }
            mail_message_html = render_to_string('substitute/mails/be_entried_notice.html', mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_bcc_list = [ask.client.email]
            mail = EmailMessage(
                subject=mail_subject, 
                body=mail_message, 
                from_email = settings.DEFAULT_FROM_EMAIL, 
                to=[settings.DEFAULT_FROM_EMAIL], 
                bcc=mail_bcc_list
                )
            mail.send()

            messages.success(request, f'応募が完了しました')

        # 依頼が確定された場合の処理
        else:
            accepted_entry = Entry.objects.get(id=request.POST['contractor'])
            ask.contractor = accepted_entry.cl
            ask.save()
            
            entries = ask.entries.all()
            for entry in entries:
                entry.state = '落選'
                entry.save()
            accepted_entry.state = ('当選')
            accepted_entry.save()

            mail_subject = '出勤者確定の通知'
            mail_context = {
                'ask': ask
            }
            mail_message_html = render_to_string('substitute/mails/contract_notice.html', mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_bcc_list = [cl.email for cl in ClassLeader.objects.all()]
            mail = EmailMessage(
                subject=mail_subject, 
                body=mail_message, 
                from_email = settings.DEFAULT_FROM_EMAIL, 
                to=[settings.DEFAULT_FROM_EMAIL], 
                bcc=mail_bcc_list
                )
            mail.send() 
        
        return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))
    
    conditions = ask.conditions.all()
    qualifications = cl.qualifications.all()
    conditions = [condition.name for condition in conditions]
    qualifications = [qualification.name for qualification in qualifications]
    is_qualified = get_is_qualified(conditions, qualifications)

    entries = ask.entries.all()
    is_entry = sum([1 if entry.cl==cl else 0 for entry in entries])

    return render(request, 'substitute/specification.html', {
        'cl': cl, 
        'ask': ask, 
        'assumed_courses': assumed_courses, 
        'conditions_json': json.dumps(conditions), 
        'conditions_all': Condition.objects.all(), 
        'entries': entries, 
        'is_qualified': is_qualified, 
        'is_entry': is_entry
    })

@login_checker
def revise(request, ask_id):
    now = datetime.datetime.now()
    ask_past = SubstituteAsk.objects.get(id=ask_id)

    if request.method == 'POST':
        form = ReviseForm(request.POST)
        if form.is_valid():
            ask_past.date = form.cleaned_data['date']
            ask_past.day = Day.objects.get(name=japanese_days[form.cleaned_data['date'].weekday()])
            ask_past.reason = form.cleaned_data['reason']
            ask_past.extra = form.cleaned_data['extra']
            ask_past.conditions.clear()
            for condition in form.cleaned_data['conditions']:
                ask_past.conditions.add(condition)
            ask_past.save()
            messages.success(request, f'代行依頼が修正されました')
            return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))

    initial_value = {
        'date': ask_past.date, 
        'reason': ask_past.reason, 
        'extra': ask_past.extra, 
        'conditions': ask_past.conditions.all()
    }
    conditions = [condition.name for condition in initial_value['conditions']]
    return render(request, 'substitute/revise.html', {
        'ask_past': ask_past, 
        'form': ReviseForm(initial=initial_value), 
        'conditions_json': json.dumps(conditions), 
        'conditions_all': Condition.objects.all()
    })

@login_checker
def make(request):
    now = datetime.datetime.now()
    cl = ClassLeader.objects.get(id=request.session['cl_id'])

    if request.method == 'POST':
        form = MakeForm(request.POST)
        if form.is_valid():
            ask = SubstituteAsk(
                date=form.cleaned_data['date'], 
                day=Day.objects.get(name=japanese_days[form.cleaned_data['date'].weekday()]), 
                client=cl, 
                contractor=None, 
                reason=form.cleaned_data['reason'], 
                extra=form.cleaned_data['extra']
            )
            ask.save()
            for condition in form.cleaned_data['conditions']:
                ask.conditions.add(condition)

            assumed_courses = ask.client.courses.filter(day=ask.day)
            mail_subject = '新規代行依頼の通知'
            mail_context = {
                'ask': ask, 
                'assumed_courses': assumed_courses, 
                'conditions': ask.conditions.all()
            }
            mail_message_html = render_to_string('substitute/mails/make_notice.html', mail_context, request)
            mail_message = strip_tags(mail_message_html)
            mail_bcc_list = [cl.email for cl in ClassLeader.objects.all()]
            mail = EmailMessage(
                subject=mail_subject, 
                body=mail_message, 
                from_email = settings.DEFAULT_FROM_EMAIL, 
                to=[settings.DEFAULT_FROM_EMAIL], 
                bcc=mail_bcc_list
                )
            mail.send() 
        
            messages.success(request, f'代行依頼が作成されました')
            return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))
            
    return render(request, 'substitute/make.html', {
        'form': MakeForm()
    })

@login_checker
def confirmAsk(request):
    now = datetime.datetime.now()
    cl = ClassLeader.objects.get(id=request.session['cl_id'])
    asks = SubstituteAsk.objects.filter(client=cl).order_by('date').reverse()
    entry_nums = [len(ask.entries.all()) for ask in asks]
    ask_values = [{'ask': ask, 'entry_num': entry_num} for (ask, entry_num) in zip(asks, entry_nums)]
    return render(request, 'substitute/confirmAsk.html', {
        'ask_values': ask_values
    })

@login_checker
def confirmEntry(request):
    now = datetime.datetime.now()
    cl = ClassLeader.objects.get(id=request.session['cl_id'])
    entries = Entry.objects.filter(cl=cl).order_by('ask__date').reverse()
    return render(request, 'substitute/confirmEntry.html', {
        'entries': entries
    })

@login_checker
def logout(request):
    request.session['cl_id'] = None
    messages.success(request, 'ログアウトが完了しました')
    return HttpResponseRedirect(reverse('substitute:login'))