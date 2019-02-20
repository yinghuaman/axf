from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=12,min_length=6,required=True,error_messages={"required":"用户账号不能为空","invalid":"用户名不合法"},widget=forms.TextInput(attrs={"class":"ccc"}))
    password = forms.CharField(max_length=16,min_length=6,widget=forms.PasswordInput)
