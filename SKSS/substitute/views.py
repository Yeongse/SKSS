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
    return 0

@login_checker
def home(request, year, month):
    return 0

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