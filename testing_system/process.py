# -*- coding: utf-8 -*-

import sqlite3

from testing_system import compile
from testing_system import verdict
from testing_system import rating_change

from time import sleep

import os
from upp import settings

import sys

from task_library import task_reader

from testing_system import sandbox


STATUS_WAIT = 'WAIT'
STATUS_IN_PROGRESS = 'IN_PROGRESS'
STATUS_READY = 'READY'

DB = 'db.sqlite3'

DELAY_BETWEEN_PROCESS = 0.1 # in seconds


def get_data_base_path(base_path):
    return base_path + os.sep + DB


def change_status(id_submission, status, data_base_path):
    connection = sqlite3.connect(data_base_path)
    connection.execute("UPDATE upp_app_submission SET status='{}' WHERE id={}".format(status, id_submission))
    connection.commit()
    connection.close()


def insert_verdict(id_submission, verdict_text, data_base_path):
    connection = sqlite3.connect(data_base_path)
    connection.execute("INSERT INTO upp_app_verdict (id_submission_id, verdict_text) VALUES ({}, '{}')".format(id_submission, verdict_text))
    connection.commit()
    connection.close()


def delete_picked_task(id_section, id_task, id_user, data_base_path):
    connection = sqlite3.connect(data_base_path)
    connection.execute('DELETE FROM upp_app_userpickedtask WHERE id_section_id={} AND id_task_id={} AND id_user_id={}'.format(id_section, id_task, id_user))
    connection.commit()
    connection.close()

def delete_closed_task(id_section, id_task, id_user, data_base_path):
    connection = sqlite3.connect(data_base_path)
    connection.execute('DELETE FROM upp_app_userclosedtasks WHERE id_section_id={} AND id_task_id={} AND id_user_id={}'.format(id_section, id_task, id_user))
    connection.commit()
    connection.close()

def insert_closed_task(id_section, id_task, id_user, data_base_path):
    connection = sqlite3.connect(data_base_path)
    connection.execute("INSERT INTO upp_app_userclosedtasks (id_user_id, id_section_id, id_task_id, is_solved) VALUES ({}, {}, {}, {})".format(id_user, id_section, id_task, 1))
    connection.commit()
    connection.close()

def update_user_rating(id_user, id_section, id_task, is_success):
    new_user_rating = rating_change.calc_new_user_rating(id_user, id_section, id_task, is_success)
    connection = sqlite3.connect(get_data_base_path(settings.BASE_DIR))
    connection.execute("UPDATE upp_app_userratinginsection SET rating='{}' WHERE id_user_id={} AND id_section_id={}".format(new_user_rating, id_user, id_section))
    connection.commit()
    connection.close()

def update_task_rating(id_user, id_task, id_section, is_success):
    new_task_rating = rating_change.calc_new_task_rating(id_user, id_section, id_task, is_success)
    connection = sqlite3.connect(get_data_base_path(settings.BASE_DIR))
    connection.execute("UPDATE upp_app_taskinsection SET rating='{}' WHERE id_user_id={} AND id_section_id={}".format(new_task_rating, id_user, id_section))
    connection.commit()
    connection.close()

def process_submission(submission, base_path):
    id_submission = submission['id']
    id_task = submission['id_task_id']
    id_section = submission['id_section_id']
    id_user = submission['id_user_id']
    data_base_path = get_data_base_path(base_path)

    change_status(id_submission, STATUS_IN_PROGRESS, data_base_path)

    try:
        absolute_build_path = compile.compile(id_submission, base_path)

        test_count = task_reader.get_tests_count(id_task)

        output_file_name = absolute_build_path + '.out'
        for test_number in range(1, test_count + 1):
            sandbox.process_test(absolute_build_path, id_task, test_number, output_file_name)
            compile.compare_outputs(id_task, task_reader.get_input_test_path(id_task, test_number), \
                                    task_reader.get_output_test_path(id_task, test_number), \
                                    output_file_name, \
                                    test_number)

        if os.path.isfile(output_file_name):
            os.remove(output_file_name)

        raise verdict.Accepted()
    except verdict.CompilationError as ce:
        insert_verdict(id_submission, str(ce), data_base_path)
    except verdict.RuntimeError as re:
        insert_verdict(id_submission, str(re), data_base_path)
    except verdict.Accepted as ac:
        insert_verdict(id_submission, str(ac), data_base_path)
        delete_closed_task(id_section, id_task, id_user, data_base_path)
        insert_closed_task(id_section, id_task, id_user, data_base_path)
        delete_picked_task(id_section, id_task, id_user, data_base_path)
        update_user_rating(id_user, id_section, id_task, True)
        update_task_rating(id_user, id_section, id_task, True)
    except verdict.MemoryLimit as ml:
        insert_verdict(id_submission, str(ml), data_base_path)
    except verdict.TimeLimit as tl:
        insert_verdict(id_submission, str(tl), data_base_path)
    except verdict.WrongAnswer as wa:
        insert_verdict(id_submission, str(wa), data_base_path)

    change_status(id_submission, STATUS_READY, data_base_path)


def process(base_path):
    iteration_number = 0
    while True:
        iteration_number += 1
        #print('iteration =', iteration_number)

        connection = sqlite3.connect(get_data_base_path(base_path))
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM upp_app_submission WHERE status='{}'".format(STATUS_WAIT))
        submission_to_process = cursor.fetchone()
        connection.close()

        if not submission_to_process is None:
            id_submission = submission_to_process['id']
            status = submission_to_process['status']
            id_section = submission_to_process['id_section_id']
            id_task = submission_to_process['id_task_id']
            id_user = submission_to_process['id_user_id']
            print('  processing submission = (id={}, status={}, id_section={}, id_task={}, id_user={})'.format(\
                    id_submission, status, id_section, id_task, id_user))
            process_submission(submission_to_process, base_path)
            print('  end of processing')

        sleep(DELAY_BETWEEN_PROCESS)


if __name__ == '__main__':
    base_path = settings.BASE_DIR
    process(base_path)