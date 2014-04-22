# coding=utf8
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from base.user import User


class SignInAccountForm(forms.Form):
    error_messages = {
        'wrong_email': _("Your email is wrong."),
        'email_not_exist': _("email is not signed up."),
        'wrong_password': _("The password is wrong."),
    }

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('password')}),
                               label=_('password'), help_text=_(''), min_length=6, max_length=20)

    def clean_email(self):
        # log.info(self.cleaned_data )
        cleaned_data = self.cleaned_data
        # log.info(cleaned_data)
        data_email = cleaned_data['email']
        user_id = User.get_user_id_by_email(data_email)
        # is_exist = User.objects.filter(email=data_email).exists()
        if user_id is None:
            raise forms.ValidationError(
                self.error_messages['email_not_exist']
            )
        return user_id

    def clean(self):
        cleaned_data = super(SignInAccountForm, self).clean()
        uid = cleaned_data.get('email', None)
        #如果没有这句判断，clean_email抛出异常后，页面也不会显示错误，很奇怪的问题
        if not uid:
            raise forms.ValidationError(
                self.error_messages['wrong_email'],
            )
        password = cleaned_data.get('password', None)
        username = User(uid).get_username()
        _user = authenticate(username=username, password=password)
        if not _user:
            raise forms.ValidationError(
                self.error_messages['wrong_password']
            )
        cleaned_data['user'] = _user
        return cleaned_data
    
class SignUpAccountForm(forms.Form):
    error_messages = {
        'nickname_exist': _("nick name is exsit"),
        'email_exist': _("email is signed up."),
        'wrong_password': _("The password repeat is wrong."),
        'register_faild': _("register faild"),
    }

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('email')}),
                             label=_('email'), help_text=_(''))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('password')}),
                               label=_('password'), help_text=_(''), min_length=6, max_length=20)
    repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': _('repeat')}),
                               label=_('repeat'), help_text=_(''), min_length=6, max_length=20)
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': _('nickname')}),
                               label=_('nickname'), help_text=_(''))

    def clean_email(self):
        # log.info(self.cleaned_data )
        data_email = self.cleaned_data['email']
        user_id = User.get_user_id_by_email(data_email)
        if user_id is None:
            return data_email
        else:
            raise forms.ValidationError(
                self.error_messages['email_exist']
            )

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.nickname_exist(nickname):
            raise forms.ValidationError(
                self.error_messages['nickname_exist']
            )
        return nickname
    
    def clean_repeat(self):
        password = self.cleaned_data.get('password', None)
        repeat = self.cleaned_data.get('repeat', None)
        if password == repeat:
            return password
        else:
            raise forms.ValidationError(
                self.error_messages['wrong_password']
            )