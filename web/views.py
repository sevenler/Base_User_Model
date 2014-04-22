from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout 

from base import settings
from base.user import User
from web.auth import SignInAccountForm, SignUpAccountForm


MAX_SESSION_EXPIRATION_TIME = getattr(settings, 'SESSION_COOKIE_AGE', 1209600)

def test(request):
    return render_to_response(
        'base.html',
        {
        },
        context_instance=RequestContext(request)
    )

def login(request, template = 'login.html'):
    if request.user.is_authenticated():
        print request.user.id
        return HttpResponseRedirect('../infor')
    
    if request.method == 'GET':
        _forms = SignInAccountForm()
        return render_to_response(
            template,
            { 
                'forms' : _forms,
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _forms = SignInAccountForm(request.POST)
        if _forms.is_valid():
            _remember_me = request.POST.get('remember_me', True)
            _user = _forms.cleaned_data['user']
#             if _user.is_active:
            auth_login(request, _user);
            if _remember_me:
                request.session.set_expiry(MAX_SESSION_EXPIRATION_TIME)
            return HttpResponseRedirect('../infor')
        else:
            return render_to_response(
                template,
                { 
                    'forms' : _forms, 
                },
                context_instance = RequestContext(request)
            )
        
def register(request, template = 'reg.html'):
    if request.method == 'GET':
        _forms = SignUpAccountForm()
        return render_to_response(
            template,
            { 
             'forms' : _forms, 
            },
            context_instance = RequestContext(request)
        )
    elif request.method == 'POST':
        _forms = SignUpAccountForm(request.POST)
        if _forms.is_valid():
            _remember_me = request.POST.get('remember_me', None)
            _email = _forms.cleaned_data['email']
            _password = _forms.cleaned_data['password']
            _nickname = _forms.cleaned_data['nickname']
            user = User.create(email = _email, password = _password, username = _nickname)
            user.set_profile(_nickname);
            _user = authenticate(username=user.get_id(), password=_password)
            if _remember_me:
                request.session.set_expiry(MAX_SESSION_EXPIRATION_TIME)
            return HttpResponseRedirect('../infor')
        else:
            return render_to_response(
                template,
                { 
                    'forms' : _forms, 
                },
                context_instance = RequestContext(request)
            )
            
def infor(request, template = 'info.html'):
    if request.user.is_authenticated():
        user_id = request.user.id
        if request.method == 'GET':
            user = User.get_user_by_id(user_id)
            return render_to_response(
                template,
                { 
                 'user' : user.read(), 
                },
                context_instance = RequestContext(request)
            )
    return HttpResponseRedirect('../login')
        
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('../login')