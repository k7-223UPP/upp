from django.contrib import admin
from upp_app.models import Task
from upp_app.models import Section
from upp_app.models import TaskInSection
from upp_app.models import Submission
from upp_app.models import Verdict
from upp_app.models import UserPickedTask
from upp_app.models import TestTask
from upp_app.models import TestTaskInSection
from upp_app.models import UserClosedTasks

admin.site.register(Task)
admin.site.register(Section)
admin.site.register(TaskInSection)
admin.site.register(Submission)
admin.site.register(Verdict)
admin.site.register(UserPickedTask)
admin.site.register(TestTask)
admin.site.register(TestTaskInSection)
admin.site.register(UserClosedTasks)