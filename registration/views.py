# -*- coding: utf-8 -*-
import re
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf

""""def registration(request):
    message = ''
    if 'error' in request.session:
        message = request.session['error']
        del request.session['error']
    context = {
        'message': message
    }
    return render(request, 'registration/registration.html', context)"""""


def registration(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if len(request.POST.get('username')) < 6 or len(request.POST.get('username')) > 18 or not re.match(
                r'^[a-zA-Z0-9]+$', request.POST.get('username')):
            args['incorrect_login'] = "Некорректный логин"
        if len(request.POST.get('password1')) < 6 or len(request.POST.get('password1')) > 18 or not re.match(
                r'^(?=\w{6,10}$)(?=.*?\d).*', request.POST.get('password1')):
            args['incorrect_password'] = "Некорректный пароль"
        if request.POST.get('password1') != request.POST.get('password2'):
            args['mismatch_passwords'] = "Пароли не совпадают"
            return redirect(registration)
        if newuser_form.is_valid():
            newuser_form.save()
            auth.authenticate(username=newuser_form['username'], password=newuser_form['password1'])
            args['success_registration'] = "Поздравляем! Вы успешно зарегистрировались в системе!"
            return render_to_response('login/login.html', args)
        else:
            args['form'] = newuser_form
            args['non_unique_login'] = "Пользователь с таким логином уже существует."
    else:
        return render_to_response('registration/registration.html', args)
    return render_to_response('registration/registration.html', args)


def regs(request):
    return render_to_response('registration/success.html')                                                              #на авторизацию
