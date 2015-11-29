# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from upp_app.models import Section, TaskInSection, Task, TestTaskInSection, TestTask, UserPickedTask, Submission
import task_library.task_reader
from .forms import SubmissionDocument
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
from testing_system import process
from upp import settings

def handle_uploaded_file(f, strg):
    with open(settings.BASE_DIR + os.sep + "sources" + os.sep + (str(strg) + ".cpp"), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def task_page(request, userPT_ID, section_ID, user_ID, task_ID):
    if request.method == 'POST':
        form = SubmissionDocument(request.POST, request.FILES)
        if form.is_valid():
            user_p_t = get_object_or_404(UserPickedTask, id=userPT_ID)
            submission_to_save = Submission(code_link = "look thisID.cpp", id_user = request.user ,id_task = user_p_t.id_task, id_section = user_p_t.id_section ,status = process.STATUS_WAIT)
            submission_to_save.save()
            handle_uploaded_file(request.FILES['docfile'], str(submission_to_save.id))
            return HttpResponseRedirect(reverse('main'))
    else:
        context = {}
        section = get_object_or_404(Section, id=section_ID)
        context['section'] = section
        context['user_is_authenticated'] = request.user.is_authenticated()
        tasks = {}
        tasks[task_library.task_reader.get_task_html(task_ID)] = task_library.task_reader.get_tutorial_html(
                task_ID)
        context['tasks'] = tasks
        form = SubmissionDocument
        context['form'] = form
        context['user_ID'] = user_ID
        context['task_ID'] = task_ID
        context['section_ID'] = section_ID
        context['userPT_ID'] = userPT_ID
        return render(request, 'task_page/task_page.html', context)