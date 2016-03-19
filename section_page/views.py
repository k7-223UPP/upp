# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from upp_app.models import UserRatingInSection, Section, TaskInSection, Task, TestTaskInSection, TestTask, UserPickedTask, UserClosedTasks, RatingHistory
import task_library.task_reader
import random
from django.shortcuts import redirect


def section_page(request, section_id):
    test_tasks = {}
    task_id = []
    test_tasks_in_sect = TestTaskInSection.objects.all().filter(id_section=section_id)
    for i in test_tasks_in_sect:
        task_id.append(i.id_test_task);
    for i in task_id:
        task = get_object_or_404(TestTask, id=i.id)
        test_tasks[task_library.task_reader.get_task_html(task.id)] = task_library.task_reader.get_tutorial_html(
            task.id)
    context = {}
    context['test_tasks'] = test_tasks
    section = get_object_or_404(Section, id=section_id)
    context['section'] = section
    context['user_is_authenticated'] = request.user.is_authenticated()
    if request.user.is_authenticated():
        try:
            user_rating_in_section = get_object_or_404(UserRatingInSection, id_user = request.user, id_section = section_id)
        except:
            user_rating_in_section = UserRatingInSection(id_user=request.user, id_section=section, rating=1000)
            RatingHistory(id_user=request.user, id_section=section, rating=1000).save()
            user_rating_in_section.save()
        context['user_rating'] = user_rating_in_section.rating
        try:
            userPT = UserPickedTask.objects.get(id_user = request.user, id_section = section)
            context['button_name'] = 'Продолжить'
        except UserPickedTask.DoesNotExist:
            tasks_in_section = TaskInSection.objects.filter(id_section=section)
            tasks_in_section_id = set(tasks_in_section.values_list('id_task', flat=True))
            # user_submissions = Submission.objects.filter(id_user = request.user, id_section = section)
            user_closed_tasks = UserClosedTasks.objects.filter(id_user=request.user, id_section=section)
            solved_tasks_id = set(user_closed_tasks.values_list('id_task', flat=True))
            suitable_tasks_id = list(tasks_in_section_id - solved_tasks_id)
            if len(suitable_tasks_id) == 0:
                context['no_tasks'] = True
            else: 
                context['button_name'] = 'Начать обучение'
        if request.POST:
            if context['button_name'] == 'Начать обучение':
                selected_task_id = random.choice(suitable_tasks_id)
                selected_task = get_object_or_404(Task, id=selected_task_id)
                userPT = UserPickedTask(id_section = section, id_user = request.user, id_task = selected_task)
                userPT.save()
            return redirect('task_page', section_id, userPT.id_task.id)
        else:
            return render(request, 'section_page/section_page.html', context)
    else:
        return render(request, 'section_page/section_page.html', context)