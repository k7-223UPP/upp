import math
import sys
import os
import django
from upp import settings
sys.path.append(os.path.join(settings.BASE_DIR, 'upp'))
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
django.setup()
import django.core.handlers.wsgi
from datetime import timedelta, datetime
application = django.core.handlers.wsgi.WSGIHandler()
from upp_app.models import UserRatingInSection, TaskInSection, Submission, Task, Section, RatingHistory, TaskRatingHistory, TestTaskRatingHistory
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def update_ratings(id_user, id_section, id_task, is_success):
    user = get_object_or_404(User, id=id_user)
    task = get_object_or_404(Task, id=id_task)
    section = get_object_or_404(Section, id=id_section)
    try:
        user_rating_in_section = get_object_or_404(UserRatingInSection, id_user=user, id_section=section)
    except:
        user_rating_in_section = UserRatingInSection(id_user=user, id_section=section, rating=1000)
        user_rating_in_section.save()
    old_user_rating = user_rating_in_section.rating
    task_in_section = get_object_or_404(TaskInSection, id_task=task, id_section=section)
    old_task_rating = task_in_section.rating
    submission_count = get_submission_count(user, task, section)
    user_factor = factor(old_user_rating, get_user_time_diff(user))
    task_factor = factor(old_task_rating, get_task_time_diff(task))
    user_exp_sc = user_expected_score(old_user_rating, old_task_rating)
    task_exp_sc = task_expected_score(old_user_rating, old_task_rating)
    if is_success:
        user_sc = user_score(submission_count)
        task_sc = task_score(submission_count)
    else:
        user_sc = 0
        task_sc = 1
    new_user_rating = new_rating(old_user_rating, user_factor, user_sc, user_exp_sc)
    new_task_rating = new_rating(old_task_rating, task_factor, task_sc, task_exp_sc)
    user_rating_in_section.rating = new_user_rating
    user_rating_in_section.save()
    task_in_section.rating = new_task_rating
    task_in_section.save()
    TaskRatingHistory(id_task=task,id_section=section, rating=new_task_rating).save()
    RatingHistory(id_user=user, id_section=section, rating=new_user_rating).save()


def get_old_user_rating(id_user, id_section):
    user_rating_in_section = get_object_or_404(UserRatingInSection, id_user=id_user, id_section=id_section)
    return user_rating_in_section.rating


def get_old_task_rating(id_task, id_section):
    task_rating_in_section = get_object_or_404(TaskInSection, id_task=id_task, id_section=id_section)
    return task_rating_in_section.rating

#это заглушка, поменть на обращение к БД
def get_user_time_diff(id_user):
    last_user_rating_changing_date = RatingHistory.objects.all().filter(id_user=id_user).order_by('-date_of_change')[0].date_of_change
    last_user_rating_changing_date = last_user_rating_changing_date.replace(tzinfo=None)
    now = datetime.now()
    time_delta = now - last_user_rating_changing_date
    return time_delta.days

#это заглушка, поменять на обращение к БД
def get_task_time_diff(id_task):
    last_task_rating_changing_date = TaskRatingHistory.objects.all().filter(id_task=id_task).order_by('-date_of_change')[0].date_of_change
    last_task_rating_changing_date = last_task_rating_changing_date.replace(tzinfo=None)
    now = datetime.now()
    time_delta = now - last_task_rating_changing_date
    return time_delta.days

def get_submission_count(id_user, id_task, id_section):
    sumbissions = Submission.objects.all().filter(id_section=id_section, id_user=id_user, id_task=id_task)
    return sumbissions.__len__()

def get_rating_diff(rating, opponent_rating):
    return (rating - opponent_rating)/200

#обобщенные функции
def new_rating(rating_old, factor, score, expected_score):
    return rating_old + factor * (score - expected_score)

def factor(rating_old, time_diff):
    return 100 * (2 * time_diff + 3) / (2 * time_diff + 6) * math.exp((-1.61) * rating_old / 2400)

def expected_score(rating_diff):
    return integrate(rating_diff)

def get_user_factor(id_user, id_section):
    return factor(get_old_user_rating(id_user, id_section),get_user_time_diff())

def get_task_factor(id_task, id_section):
    return factor(get_old_task_rating(id_task, id_section),get_task_time_diff())

#функции для пользователя
def user_score(submission_count):
    return 1/submission_count if submission_count!=0 else 1

def user_expected_score(user_rating, task_rating):
    return expected_score(get_rating_diff(user_rating, task_rating))

#функции для задачи
def task_score(submission_count):
    return 1 - user_score(submission_count)

def task_expected_score(user_rating, task_rating):
    return 1 - user_expected_score(user_rating, task_rating)

#функция, которая считает интеграл
def integrate(upper):
    delta = 0.001
    lower = -20
    current = lower
    sum = 0
    while (current < upper):
        sum = sum + delta * ( math.sqrt(math.pi) / 2) * math.exp((-1) * (current ** 2) * (math.pi ** 2)/ 4)
        current += delta
    return sum