from django import forms
from pkg_resources import require
from .models import Course, ClassLeader, Condition, SubstituteAsk, Entry

class LoginForm(forms.Form):
    identification = forms.CharField(label='職員ID or メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), min_length=4)

class InitializeForm(forms.Form):
    password1 = forms.CharField(label='パスワード(4文字以上)', widget=forms.PasswordInput(), min_length=4)
    password2 = forms.CharField(label='パスワードをもう一度', widget=forms.PasswordInput(), min_length=4)



# class PersonalForm(forms.Form):
#     name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
#     password1 = forms.CharField(label="パスワード", widget=forms.PasswordInput(), min_length=4)
#     password2 = forms.CharField(label="パスワードをもう一度", widget=forms.PasswordInput(), min_length=4)
#     email = forms.CharField(label="メールアドレス", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))

# class RegisterForm(forms.Form):
#     name = forms.CharField(label="ユーザ名", widget=forms.TextInput(attrs={"placeholder": "姓名を漢字で空白無しで"}))
#     email = forms.CharField(label="メールアドレス", widget=forms.TextInput(attrs={"placeholder": "メールアドレス"}))
#     is_admin = forms.BooleanField(required=False)

# class DeleteForm(forms.Form):
#     delete = forms.ModelChoiceField(label="削除する従業員", queryset=Worker.objects.all())

# class ReviseForm(forms.Form):
#     name = forms.CharField(label="名前")
#     date = forms.DateField(label="日付", widget=forms.TextInput(attrs={"placeholder": "XXXX-YY-ZZ"}))
#     startTime = forms.CharField(label="開始時刻", widget=forms.TextInput(attrs={"placeholder": "XX:YY"}))
#     endTime = forms.CharField(label="終了時刻", widget=forms.TextInput(attrs={"placeholder": "XX:YY"}))
#     specification = forms.CharField(label="詳細内容", widget=forms.Textarea())
#     type = forms.ChoiceField(label="業務種別", choices=(("CL外業務", "CL外業務"), ("CL業務", "CL業務"), ("その他", "その他")))
#     capacity = forms.IntegerField(label="募集人数")
#     extra = forms.CharField(label="特筆事項", widget=forms.Textarea(), required=False)

# # デフォルトのクエリセットにはフォームから送信された値が存在するようにしておく. 
# class ReassignForm(forms.Form):
#     add = forms.ModelChoiceField(label="出勤者の追加", required=False, queryset=Worker.objects.all())
#     remove = forms.ModelChoiceField(label="出勤者の削除", required=False, queryset=Worker.objects.all())

# class MakeForm(forms.Form):
#     name = forms.CharField(label="名前")
#     date = forms.DateField(label="日付", widget=forms.TextInput(attrs={"placeholder": "XXXX-YY-ZZ"}))
#     startTime = forms.CharField(label="開始時刻", widget=forms.TextInput(attrs={"placeholder": "XX:YY"}))
#     endTime = forms.CharField(label="終了時刻", widget=forms.TextInput(attrs={"placeholder": "XX:YY"}))
#     specification = forms.CharField(label="詳細内容", widget=forms.Textarea())
#     type = forms.ChoiceField(label="業務種別", choices=(("CL外業務", "CL外業務"), ("CL業務", "CL業務"), ("その他", "その他")))
#     capacity = forms.IntegerField(label="募集人数")
#     extra = forms.CharField(label="特筆事項", widget=forms.Textarea(), required=False)

# class RecallForm(forms.Form):
#     pastTask = forms.ModelChoiceField(label="過去の業務を呼び出す", queryset=Task.objects.all())