from django.contrib import admin
from tasker.models import TaskManager, Task
# Register your models here.
admin.site.register(TaskManager)
admin.site.register(Task)