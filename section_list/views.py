# -*- coding: utf-8 -*-

from django.shortcuts import render
from upp_app.models import Section

def sectionlist(request):
    sections = Section.objects.all()
    context = {
        'sections': sections
    }
    return render(request, 'section_list/section_list.html', context)


