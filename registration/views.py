# -*- coding: utf-8 -*-
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf


def registration(request):
    message = ''
    if ('error' in request.session):
        message = request.session['error']
        del request.session['error']
    context = {
        'message': message
    }
    return render(request, 'registration/registration.html', context)


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if (len(request.POST.get('username'))<6 or len(request.POST.get('username'))>18 or not re.match(r'^[a-zA-Z0-9]+$', request.POST.get('username'))):
            message = "Некорректный логин."
            request.session['error'] = message
            return redirect(registration)
        if (len(request.POST.get('password1'))<6 or len(request.POST.get('password1'))>18 or not re.match(r'^(?=[0-9+а-яА-ЯёЁa-zA-Z0-9]*(?=.*?\d).*)', request.POST.get('password1'))):
            message = "Некорректный пароль"
            request.session['error'] = message
            return redirect(registration)
        if request.POST.get('password1') != request.POST.get('password2'):
            message = "Пароли не совпадают"
            request.session['error'] = message
            return redirect(registration)
        if newuser_form.is_valid():
            newuser_form.save()
            auth.authenticate(username = newuser_form['username'], password = newuser_form['password1'])
            return redirect(regs)

        else:
            args['form'] = newuser_form
            message = "Пользователь с таким логином уже существует"
            request.session['error'] = message
            return redirect(registration)


def exist(request):
    return render_to_response('registration/error_message1.html')

def regs(request):
    return render_to_response('registration/success.html')
def index(request):
    return render_to_response('registration/index.html')
