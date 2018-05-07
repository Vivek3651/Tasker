from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
# Create your models here.

class CustomModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True

class TaskTag(CustomModel):
	name = models.CharField(max_length=50)
	def __str__(self):
	    return self.name

class Task(CustomModel):
	task_name = models.CharField(max_length=100)
	task_description = models.TextField(max_length=1000, blank=True)
	tags = models.ManyToManyField(TaskTag, blank=True)

	def __str__(self):
	    return self.task_name

class TaskManager(CustomModel):
	
	UNDONE = 'U'
	DONE = 'D'
	INACTIVE = 'I'

	task = models.ForeignKey(Task, on_delete=CASCADE)
	task_owner = models.ForeignKey(User, related_name='task_owner')

	task_status_choices = (
        (UNDONE, 'Undone Task'),
        (DONE, 'Completed Task'),
        (INACTIVE, 'Inactive Task'),
    )
	task_status = models.CharField(max_length=2, choices=task_status_choices, default=UNDONE)
	completed_by = models.ForeignKey(User,null=True, blank=True, related_name='completed_by')
	notes = models.TextField(max_length=1000, blank=True)
