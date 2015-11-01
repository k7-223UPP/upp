from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    rating = models.IntegerField()
    name = models.CharField(max_length=50)
    datalink = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class TaskInSection(models.Model):
    id_section = models.ForeignKey(Section)
    id_task = models.ForeignKey(Task)



