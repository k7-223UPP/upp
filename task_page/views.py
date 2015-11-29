# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from upp_app.models import Section, TaskInSection, Task, UserPickedTask, Submission
import task_library.task_reader
from .forms import SubmissionDocument

from django.contrib import auth
from django.contrib.auth.models import User
from testing_system import process
import os
from upp import settings


def handle_uploaded_file(f, strg):
    with open(settings.BASE_DIR + os.sep + "sources" + os.sep + (str(strg) + ".cpp"), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def task_page(request, id_section, id_task):
    if request.method == 'POST':
        form = SubmissionDocument(request.POST, request.FILES)
        if form.is_valid():
            submission_to_save = Submission(id_user=request.user, id_task=id_task, id_section=id_section, status=process.STATUS_WAIT)
            submission_to_save.save()
            handle_uploaded_file(request.FILES['docfile'], str(submission_to_save.id))
        return redirect('main')

    # request.method == 'GET'
    if not request.user.is_authenticated():
        return redirect('access')
    else:
        if UserPickedTask.Objects.all().filter(id_section=id_section, id_user=User.Objects.all().filter(username=auth.get_user(request))) == None:
            if Submission.Objects.all().filter(id_section=id_section, id_user=User.Objects.all().filter(username=auth.get_user(request)), id_task=id_task) == None:
                return redirect('access')
            else:
                tasks = {}
                for i in id_task:
                    task = get_object_or_404(Task, id=i.id)
                    tasks[task_library.task_reader.get_task_html(task.id)] = task_library.task_reader.get_tutorial_html(
                        task.id)
                context = {}
                context['tasks'] = tasks
                context['section'] = get_object_or_404(Section, id=id_section)
                return render(request, 'task_page/task_page_close.html')
        else:
            tasks = {}
            for i in id_task:
                task = get_object_or_404(Task, id=i.id)
                tasks[task_library.task_reader.get_task_html(task.id)] = task_library.task_reader.get_tutorial_html(
                    task.id)
            context = {}
            context['tasks'] = tasks
            context['section'] = get_object_or_404(Section, id=id_section)
            return render(request, 'task_page/task_page_open.html', context)