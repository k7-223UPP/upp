# -*- coding: utf-8 -*-

from upp_app.models import Submission
from upp_app.models import Verdict

from testing_system import compile
from testing_system import verdict

STATUS_WAIT = 'WAIT'
STATUS_IN_PROGRESS = 'IN_PROGRESS'
STATUS_READY = 'READY'

def process_submission(submission):
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

if __name__ == '__main__':
    while True:
        wait_submissions = Submission.objects.filter(status = STATUS_WAIT)
        submission_to_process = wait_submissions.first()
        if submission_to_process is None:
            continue
        process_submission(submission_to_process)