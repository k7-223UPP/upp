# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from upp_app.models import Section, TaskInSection, Task, TestTaskInSection, TestTask
import task_library.task_reader


def section_page(request, section_id):
    test_tasks = {}
    task_id = []
    task_in_sect = TestTaskInSection.objects.all().filter(id_section=section_id)
    for i in task_in_sect:
        task_id.append(i.id_test_task);
    for i in task_id:
        task = get_object_or_404(TestTask, id=i.id)
        test_tasks[task_library.task_reader.get_task_html(task.id)] = task_library.task_reader.get_tutorial_html(
            task.id)
    context = {}
    context['test_tasks'] = test_tasks
    context['section'] = get_object_or_404(Section, id=section_id)
    return render(request, 'section_page/section_page.html', context)
