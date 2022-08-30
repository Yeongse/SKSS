from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.db.models import Q

# Create your views here.
import datetime
now = datetime.datetime.now()

def login_checker(func):
    def checker(request, **kwargs):
        if 'cl_id' not in request.session:
            return HttpResponseRedirect(reverse('substitute:login'))
        else:
            return func(request, **kwargs)
    return checker

@login_checker
def index(request):
    return HttpResponseRedirect(reverse('substitute:home', args=[now.year, now.month]))

@login_checker
def login(request):
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
def confirmApply(request):
    return 0

@login_checker
def logout(request):
    return 0