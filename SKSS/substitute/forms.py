from django import forms
from pkg_resources import require
from .models import Course, ClassLeader, Condition, SubstituteAsk, Entry

class LoginForm(forms.Form):
    identification = forms.CharField(label='職員ID or メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), min_length=4)

class InitializeForm(forms.Form):
    password1 = forms.CharField(label='パスワード(4文字以上)', widget=forms.PasswordInput(), min_length=4)
    password2 = forms.CharField(label='パスワードをもう一度', widget=forms.PasswordInput(), min_length=4)