from django.contrib import admin
from upp_app.models import Task
from upp_app.models import Section
from upp_app.models import TaskInSection

admin.site.register(Task)
admin.site.register(Section)
admin.site.register(TaskInSection)