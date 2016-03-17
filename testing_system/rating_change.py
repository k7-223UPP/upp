import math
import os

import sqlite3

from upp import settings

DB = 'db.sqlite3'
def get_data_base_path():
    return settings.BASE_DIR + os.sep + DB

def get_old_user_rating(id_user, id_section):
    connection = sqlite3.connect(get_data_base_path())
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM upp_app_userratinginsection WHERE id_user_id='{}' AND id_section_id={}".format(id_user, id_section))
    s= cursor.fetchone()
    print("old_user_rating= "+ str(s))
    return s[1]

def get_old_task_rating(id_task, id_section):
    connection = sqlite3.connect(get_data_base_path())
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM upp_app_taskinsection WHERE id_task_id='{}' AND id_section_id={}".format(id_task, id_section))
    s= cursor.fetchone()
    print("old_task_rating= "+ str(s))
    return s[3]

#это заглушка, поменть на обращение к БД
def get_user_time_diff():
    return 1
#это заглушка, поменть на обращение к БД
def get_task_time_diff():
    return 1

def get_submission_count(id_user, id_task, id_section):
    connection = sqlite3.connect(get_data_base_path())
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM upp_app_submission WHERE id_user_id = {} AND id_task_id='{}' AND id_section_id={}".format(id_user, id_task, id_section))
    return cursor.fetchall().__len__()

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

def calc_new_user_rating(id_user, id_section, id_task, is_success):
    old_user_rating = get_old_user_rating(id_user, id_section)
    task_rating = get_old_task_rating(id_task, id_section)
    factor = get_user_factor(id_user, id_section)
    submission_count = get_submission_count(id_user, id_task, id_section)
    exp_score = user_expected_score(old_user_rating, task_rating)
    new_user_rating= new_rating(old_user_rating, factor, user_score(submission_count) if is_success else 0, exp_score)
    print("new_user_rating= "+ str(new_user_rating))
    return new_user_rating

#функции для задачи
def task_score(submission_count):
    return 1 - user_score(submission_count)

def task_expected_score(user_rating, task_rating):
    return 1 - user_expected_score(user_rating, task_rating)

def calc_new_task_rating(id_user, id_section, id_task, is_success):
    old_task_rating = get_old_task_rating(id_task, id_section)
    user_rating = get_old_user_rating(id_user, id_section)
    factor = get_task_factor(id_task, id_section)
    submission_count = get_submission_count(id_user, id_task, id_section)
    exp_score = task_expected_score(user_rating, old_task_rating)
    new_task_rating= new_rating(old_task_rating, factor, user_score(submission_count) if is_success else 0, exp_score)
    print("new_task_rating= "+ str(new_task_rating))
    return new_task_rating
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