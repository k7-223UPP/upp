# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from upp_app.models import Section, TaskInSection, Task, TestTaskInSection, TestTask, UserPickedTask, Submission
import task_library.task_reader
from .forms import SubmissionDocument
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def handle_uploaded_file(f, strg):
    with open('/Users/Misha/PycharmProjects/untitled folder/upp/sources/' + (str(strg) + ".cpp"), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def task_page(request, userPT_ID, section_ID, user_ID, task_ID):
    if request.method == 'POST':
        form = SubmissionDocument(request.POST, request.FILES)
        if form.is_valid():
            userPT = get_object_or_404(UserPickedTask, id=userPT_ID)
            SubmissionToSave = Submission(code_link = "look thisID.cpp", id_user = request.user ,id_task = userPT.id_task, id_section = userPT.id_section ,status = "PROGRESS")
            SubmissionToSave.save()
            handle_uploaded_file(request.FILES['docfile'], str(SubmissionToSave.id))
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