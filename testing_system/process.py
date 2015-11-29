# -*- coding: utf-8 -*-

import sqlite3

from testing_system import compile
from testing_system import verdict

from time import sleep

import os

import sys


STATUS_WAIT = 'WAIT'
STATUS_IN_PROGRESS = 'IN_PROGRESS'
STATUS_READY = 'READY'


def process_submission(submission, connection, cursor):
    submission.status = STATUS_IN_PROGRESS
    submission.save()
    id_submission = submission.id
    try:
        absolute_build_path = compile.compile(id_submission)
        # code to check
    except verdict.CompilationError as ce:
        submission_verdict = Verdict(id_submission=id_submission, verdict_text=str(ce))
        submission_verdict.save()
    submission.status = STATUS_READY
    submission.save()


def process(base_path):
    DB = 'db.sqlite3'
    data_base_path = base_path + os.sep + DB
    while True:
        connection = sqlite3.connect(data_base_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Submission WHERE Status = {}'.format(STATUS_WAIT))

        submission_to_process = cursor.fetchone()

        if not submission_to_process is None:
            process_submission(submission_to_process, connection, cursor)
            connection.commit()

        connection.close()
        sleep(0.01) # delay between checking = 10 milliseconds


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print('incorrect usage!')
        print('usage: process base_path')
        exit(0)

    base_path = sys.argv[0]
    process(base_path)