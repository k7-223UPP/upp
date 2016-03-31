# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from upp_app.models import Section, Task, UserPickedTask, Submission, UserClosedTasks, TaskInSection, UserRatingInSection
import task_library.task_reader
from .forms import SubmissionDocument
from testing_system import process
from rating_changing import rating_change
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
            task_current = get_object_or_404(Task, id=id_task)
            section_current = get_object_or_404(Section, id=id_section)
            submission_to_save = Submission(id_user=request.user, id_task=task_current, id_section=section_current, status=process.STATUS_WAIT, )
            submission_to_save.save()
            handle_uploaded_file(request.FILES['docfile'], str(submission_to_save.id))
        return redirect('submissions')

    # request.method == 'GET'
    if not request.user.is_authenticated():
        return redirect('access')
    else:
        tasks = {}
        context = {}
        user_rating_in_section = get_object_or_404(UserRatingInSection, id_user = request.user, id_section = id_section)
        context['user_rating_in_section'] = user_rating_in_section.rating
        for i in id_task:
            task = get_object_or_404(Task, id=i)
            tasks[task_library.task_reader.get_task_html(task.id)] = task_library.task_reader.get_tutorial_html(task.id)
            id_section_obj  = get_object_or_404(Section, id=id_section)
            try:
                task_in_section = get_object_or_404(TaskInSection, id_task=task, id_section= id_section_obj)
            except:
                None
            else:
                task_rating = task_in_section.rating
            context['task_rating'] = task_rating
        context['tasks'] = tasks
        context['section'] = get_object_or_404(Section, id=id_section)
        context['show_tutorial'] = False
        context['task_id'] = id_task
        form = SubmissionDocument()
        context['form'] = form
        if not (UserPickedTask.objects.all().filter(id_section=id_section, id_user=request.user.id, id_task=id_task)):
            if not (UserClosedTasks.objects.all().filter(id_section=id_section, id_user=request.user.id, id_task=id_task)):
                return redirect('access')
            else:
                context['show_tutorial'] = True
                return render(request, 'task_page/task_page.html', context)
        else:
            return render(request, 'task_page/task_page.html', context)

def task_page_close(request, id_section, id_task):
    if request.method == 'POST':
        task_current = get_object_or_404(Task, id=id_task)
        section_current = get_object_or_404(Section, id=id_section)
        task_to_close = UserClosedTasks(id_user=request.user, id_section=section_current, id_task=task_current, is_solved=False)
        task_to_close.save()
        user_picked_task = get_object_or_404(UserPickedTask, id_section=section_current, id_task=task_current, id_user=request.user)
        user_picked_task.delete()
        rating_change.update_ratings(request.user.id, id_section, id_task, False)
        return redirect('section_page', id_section)
    else:
        return redirect('access')

