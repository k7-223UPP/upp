from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=50)
    datalink = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1500, default='')
    short_description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class TaskInSection(models.Model):
    id_section = models.ForeignKey(Section)
    id_task = models.ForeignKey(Task)
    rating = models.IntegerField()

    def __str__(self):
        return 'task=' + str(self.id_task) + '; section=' + str(self.id_section)

class Submission(models.Model):
    id_user = models.ForeignKey(User)
    id_task = models.ForeignKey(Task)
    id_section = models.ForeignKey(Section)
    status = models.CharField(max_length=10)

class Verdict(models.Model):
    id_submission = models.ForeignKey(Submission)
    verdict_text = models.CharField(max_length=15)

class UserPickedTask(models.Model):
    id_section = models.ForeignKey(Section)
    id_task = models.ForeignKey(Task)
    id_user = models.ForeignKey(User)

    def __str__(self):
        return 'user=' + str(self.id_user) + '; section=' + str(self.id_section) + '; task=' + str(self.id_task)

class TestTask(models.Model):
    name = models.CharField(max_length=50)
    datalink = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TestTaskInSection(models.Model):
    id_section = models.ForeignKey(Section)
    id_test_task = models.ForeignKey(TestTask)
    rating = models.IntegerField()

    def __str__(self):
        return 'task=' + str(self.id_test_task) + '; section=' + str(self.id_section)

class UserClosedTasks(models.Model):
    id_user = models.ForeignKey(User)
    id_section = models.ForeignKey(Section)
    id_task = models.ForeignKey(Task)
    is_solved = models.BooleanField()
    reason = models.CharField(max_length=300)
    user_rating_change = models.IntegerField()
    task_rating_change = models.IntegerField()

    def __str__(self):
        return 'user=' + str(self.id_user) + '; section=' + str(self.id_section) + '; task=' + str(self.id_task) + '; is_solved=' + str(self.is_solved)

class UserRatingInSection(models.Model):
    id_user = models.ForeignKey(User)
    id_section = models.ForeignKey(Section)
    rating = models.IntegerField(default=1000)
    def __str__(self):
        return 'user=' + str(self.id_user) + '; section=' + str(self.id_section) + '; rating=' + str(self.rating)

class RatingHistory(models.Model):
    id_user = models.ForeignKey(User)
    id_section = models.ForeignKey(Section)
    date_of_change = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField()

    def __str__(self):
        return 'user=' + str(self.id_user) + '; section=' + str(self.id_section) + '; date=' + str(self.date_of_change) + '; rating=' + str(self.rating)