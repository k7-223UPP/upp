# -*- coding: utf-8 -*-
from itertools import chain
import re
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from upp_app.models import Submission, Task, Verdict, Section, RatingHistory, UserClosedTasks, UserRatingInSection
from task_library import task_reader
from operator import itemgetter

def private_data(request):

    if not request.user.is_authenticated():
        return redirect('access')
    args = fill_menu(request.get_full_path())
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
                user = auth.authenticate(username=username, password=passwordnew)
                auth.login(request, user)
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
    args = fill_menu(request.get_full_path())

    if not request.user.is_authenticated():
        return redirect('access')
    pages = []
    submission = Submission.objects.all().filter(id_user=auth.get_user(request).id).order_by('-id')

    SUBMISSION_PER_PAGE = 10
    paginator = Paginator(submission, SUBMISSION_PER_PAGE) # Show 25 contacts per page

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

    args['contacts'] = contacts
    args['pages'] = pages
    return render(request, 'personal_account/submissions.html', args)

def general_statistics(request):
    if not request.user.is_authenticated():
        return redirect('access')
    args = fill_menu(request.get_full_path())
    statistics_args = get_statistics(user_id=auth.get_user(request).id)
    args.update(statistics_args)
    return render(request, 'personal_account/general_statistics.html', args)

def section_statistics(request, section_id):
    if not request.user.is_authenticated():
        return redirect('access')
    args = fill_menu(request.get_full_path())
    args['no_rating_in_section'] = False
    has_rating_in_section = UserRatingInSection.objects.filter(id_section_id=section_id, id_user_id=auth.get_user(request).id)
    if len(has_rating_in_section) > 0:
        statistics_args = get_statistics(user_id=auth.get_user(request).id, id_section=section_id)
        args.update(statistics_args)
    else:
        args['no_rating_in_section'] = True

    return render(request, 'personal_account/section_statistics.html', args)

def fill_menu(full_path):
    args = {}
    args['sections'] = Section.objects.all()
    args['private_data_class'] = 'btn'
    args['submissions_class'] = 'btn'
    args['general_statistics_class'] = 'btn'
    if full_path == '/personal_account/':
        args['private_data_class'] += ' active'
    elif re.match(r'^/personal_account/submissions*', full_path):
        args['submissions_class'] += ' active'
    elif full_path == '/personal_account/general_statistics':
        args['general_statistics_class'] += ' active'

    return args

def get_statistics(user_id, id_section=0):
    # data for diagram
    args = {}
    args['rating_data'] = []
    if id_section == 0:
        section_id_list = Section.objects.all().values_list('id', flat=True)
        args['test'] = section_id_list
        rating_in_section = {}
        sum_of_ratings = 0
        section_amount = 0
        for section_id in section_id_list:
            rating_in_section[section_id] = -1

        rating_change_data = RatingHistory.objects.filter(id_user=user_id).order_by('date_of_change')
        rating_list = []
        for obj in rating_change_data:
            if rating_in_section[obj.id_section_id] == -1:
                section_amount += 1
                sum_of_ratings -= 1
            sum_of_ratings += obj.rating - rating_in_section[obj.id_section_id]
            rating_in_section[obj.id_section_id] = obj.rating

            rating_list.append(sum_of_ratings / section_amount)

        date_of_change_list = rating_change_data.values_list('date_of_change', flat=True)
        args['rating_data'] = map(lambda x,y: [x,y], date_of_change_list, rating_list)
    else:
        section = get_object_or_404(Section, id=id_section)
        rating_change_data = RatingHistory.objects.filter(id_user=user_id, id_section=section).order_by('date_of_change')
        rating_list = rating_change_data.values_list('rating', flat=True)
        date_of_change_list = rating_change_data.values_list('date_of_change', flat=True)
        args['rating_data'] = map(lambda x,y: [x,y], date_of_change_list, rating_list)
    closed_tasks = UserClosedTasks.objects.all()

    # ----------------------
    # second part of statistics

    if id_section == 0:
        closed_tasks = closed_tasks.filter(id_user=user_id)
    else:
        section = get_object_or_404(Section, id=id_section)
        closed_tasks = closed_tasks.filter(id_user=user_id, id_section=section)

    args['solved'] = len(closed_tasks.filter(is_solved=True))
    args['not_solved'] = len(closed_tasks.filter(is_solved=False))
    args['whole'] = args['not_solved'] + args['solved']
    if args['whole'] != 0:
        args['solved_per'] = args['solved'] / args['whole'] * 100
        args['not_solved_per'] = 100 - args['solved_per']
    else:
        args['solved_per'] = 0
        args['not_solved_per'] = 0

    # -------------------
    # last part

    rating_in_section = UserRatingInSection.objects.all().order_by('id_user')
    args['user_position'] = 0
    args['amount_of_users'] = -1
    if id_section == 0:
        general_rating = []
        rating_sum = 0
        cur_id = -1
        section_amount = 0
        for obj in rating_in_section:
            if cur_id == obj.id_user_id:
                rating_sum += obj.rating
                section_amount += 1
            else:
                if cur_id != -1:
                    general_rating.append((cur_id, rating_sum / section_amount))
                rating_sum = obj.rating
                section_amount = 1
                cur_id = obj.id_user_id
        general_rating.append((cur_id, rating_sum / section_amount))
        pos = 1
        pos_acc = 0
        cur_rating = -1
        for (id_user, rating) in sorted(general_rating, key=itemgetter(1), reverse=True):
            if id_user == user_id:
                break
            if cur_rating != rating:
                pos += 1 + pos_acc
                pos_acc = 0
            else:
                pos_acc += 1

        args['user_position'] = pos
        args['amount_of_users'] = len(general_rating)
    else:
        section = get_object_or_404(Section, id=id_section)
        rating_in_section = rating_in_section.filter(id_section=section).order_by('-rating')
        pos = 1
        pos_acc = 0
        cur_rating = -1
        for obj in rating_in_section:
            if obj.id_user_id == user_id:
                break
            if cur_rating != obj.rating:
                pos += 1 + pos_acc
                pos_acc = 0
            else:
                pos_acc += 1

        args['user_position'] = pos
        args['amount_of_users'] = len(rating_in_section)

    return args

