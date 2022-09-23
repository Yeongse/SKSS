from django import forms
from pkg_resources import require
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Course, ClassLeader, Condition, SubstituteAsk, Entry

class LoginForm(forms.Form):
    identification = forms.CharField(label='職員ID or メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), min_length=4)

class InitializeForm(forms.Form):
    password1 = forms.CharField(label='パスワード(4文字以上)', widget=forms.PasswordInput(), min_length=4)
    password2 = forms.CharField(label='パスワードをもう一度', widget=forms.PasswordInput(), min_length=4)

class MakeForm(forms.Form):
    date = forms.DateField(label='代行日時', widget=DatePickerInput(format='%Y-%m-%d', options={'locale': 'ja', 'dayViewHeaderFormat': 'YYYY年 MMMM',}))
    reason = forms.CharField(label='代行理由', widget=forms.Textarea())
    extra = forms.CharField(label='特筆事項', required=False, widget=forms.Textarea())
    conditions = forms.ModelMultipleChoiceField(label='応募条件', required=False, widget=forms.CheckboxSelectMultiple, queryset=Condition.objects.all())

class ReviseForm(forms.Form):
    date = forms.DateField(label='代行日時', widget=DatePickerInput(format='%Y-%m-%d', options={'locale': 'ja', 'dayViewHeaderFormat': 'YYYY年 MMMM',}))
    reason = forms.CharField(label='代行理由', widget=forms.Textarea())
    extra = forms.CharField(label='特筆事項', required=False, widget=forms.Textarea())
    conditions = forms.ModelMultipleChoiceField(label='応募条件', required=False, widget=forms.CheckboxSelectMultiple, queryset=Condition.objects.all())