# -*- coding: utf-8 -*-
from itertools import chain
import re
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from upp_app.models import Submission, Task, Verdict
from task_library import task_reader


def private_data(request):
    if not request.user.is_authenticated():
        return redirect('access')
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        if 'passwordold' in request.POST:
            username = auth.get_user(request)
            user = auth.authenticate(username=username, password=request.POST.get('passwordold'))
            passwordnew = request.POST.get('passwordnew1')
            if user is not None:
                if len(passwordnew) < 6 or len(passwordnew) > 18 or not re.match(r'^(?=\w{6,10}$)(?=.*?\d).*',
                                                                                 passwordnew):
                    args['incorrect_password'] = "Некорректный пароль"
                    return render(request, 'personal_account/private_data.html', args)
                if passwordnew != request.POST.get('passwordnew2'):
                    args['mismatch_passwords'] = "Пароли не совпадают"
                    return render(request, 'personal_account/private_data.html', args)
                if request.POST.get('passwordold') == passwordnew:
                    args['oldpass_equal_newpass'] = "Старый и новый пароли совпадают"
                    return render(request, 'personal_account/private_data.html', args)
                user.set_password(passwordnew)
                user.save()
                args['success_edit_newpassword'] = "Поздравляем! Ваш пароль успешно изменен!"
                return render(request, 'personal_account/private_data.html', args)
            else:
                args['password_error'] = 'Неверный старый пароль'
                return render(request, 'personal_account/private_data.html', args)
        if 'username' in request.POST:
            username = auth.get_user(request)
            newusername = request.POST.get('username')
            user1 = User.objects.get(username=username)
            try:
                user2 = User.objects.get(username=newusername)
            except User.DoesNotExist:
                if len(newusername) < 6 or len(newusername) > 18 or not re.match(r'^[a-zA-Z0-9]+$', newusername):
                    args['incorrect_login'] = "Некорректный логин"
                    return render(request, 'personal_account/private_data.html', args)
                if username == newusername:
                    args['oldlogin_equal_newlogin'] = "Старый и новый логины совпадают"
                    return render(request, 'personal_account/private_data.html', args)
                user1.username = newusername
                user1.save()
                args['success_edit_newlogin'] = "Поздравляем! Ваш логин успешно изменен!"
                return redirect('private_data')
            args['non_unique_login'] = "Пользователь с таким логином уже существует."
            return render(request, 'personal_account/private_data.html', args)

    else:
        return render(request, 'personal_account/private_data.html', args)

def submissions(request):
    if not request.user.is_authenticated():
        return redirect('access')
    pages = []
    submission = Submission.objects.all().filter(id_user=auth.get_user(request).id).order_by('id')

    paginator = Paginator(submission, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    for i in range(1, paginator.num_pages + 1):
        pages.append(i)

    for contact in contacts:
        contact.title_task = task_reader.get_task_title(contact.id_task_id)

        verdict = Verdict.objects.all().filter(id_submission=contact.id)
        if verdict:
            contact.verdict = verdict[0].verdict_text
        else:
            contact.verdict = ''

    return render(request, 'personal_account/submissions.html', {"contacts": contacts, "pages": pages})
