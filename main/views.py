from django.http import HttpResponseRedirect
from django.shortcuts import render
import task_library.task_reader

def home(request):
    args = {}
    args['task'] = task_library.task_reader.get_task_html(1)
    args['tutorial'] = task_library.task_reader.get_tutorial_html(1)
    return render(request, 'main/home.html', args)

