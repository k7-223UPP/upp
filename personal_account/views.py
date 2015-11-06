# -*- coding: utf-8 -*-
import re
from django.shortcuts import render_to_response, render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf


def personal_account(request):
    if request.user.is_authenticated():
        return render(request, 'personal_account/personal_account.html')
    else:
        return redirect('main')


def private_data(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        edituser_form = UserCreationForm(request.POST)

        if len(request.POST.get('username')) < 6 or len(request.POST.get('username')) > 18 or not re.match(
                r'^[a-zA-Z0-9]+$', request.POST.get('username')):
            args['incorrect_login'] = "Некорректный логин"
            return render_to_response('personal_account/private_data.html', args)

        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if len(request.POST.get('passwordnew1')) < 6 or len(request.POST.get('passwordnew1')) > 18 or not re.match(
                    r'^(?=\w{6,10}$)(?=.*?\d).*', request.POST.get('passwordnew1')):
                args['incorrect_password'] = "Некорректный пароль"
                return render_to_response('personal_account/private_data.html', args)
            if request.POST.get('passwordnew1') != request.POST.get('passwordnew2'):
                args['mismatch_passwords'] = "Пароли не совпадают"
                return render_to_response('personal_account/private_data.html', args)
            if edituser_form.is_valid():
                edituser_form.save()
                auth.authenticate(username=edituser_form['username'], password=edituser_form['password1'])
                args['success_edit'] = "Поздравляем! Ваши данные успешно изменены!"
                return render_to_response('personal_account/private_data.html', args)
            else:
                args['form'] = edituser_form
                args['non_unique_login'] = "Пользователь с таким логином уже существует."
                return render_to_response('personal_account/private_data.html', args)
        else:
            args['login_error'] = 'Неверный пароль и/или логин'
    else:
        return render(request, 'personal_account/private_data.html', args)
