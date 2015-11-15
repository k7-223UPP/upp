# coding=utf-8
from django.contrib.auth import logout

from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth
from django.template.context_processors import csrf


def login(request):
    if request.user.is_authenticated():
        return redirect('access')
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            args['login_error'] = 'Неверный пароль и/или логин'
            return render_to_response('login/login.html', args)
    else:
        return render_to_response('login/login.html', args)


def logout_view(request):
    if not request.user.is_authenticated():
        return redirect('access')
    logout(request)
    return redirect('main')


def access(request):
    return render(request, 'login/access.html')


def process(request):
    return render(request, 'login/process.html')
