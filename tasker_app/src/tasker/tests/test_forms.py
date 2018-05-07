from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from ..models import Task, TaskManager
from ..forms import TaskForm

class TaskModelTestCase(TestCase):
	def test_validate_form(self):
		task_fields = {
			"task_name":"random",
			"task_description":"description",
		}
		task_obj = Task.objects.create(**task_fields)
		form = TaskForm(data=task_fields)
		self.assertTrue(form.is_valid())
		self.assertNotEqual(form.cleaned_data.get("task_description"), "some stuff")
		self.assertEqual(form.cleaned_data.get("task_name"), task_obj.task_name)

	def test_invalidate_form(self):
		task_fields = {
			"task_name":"random",
			"task_description":"description",
		}
		task_obj = Task.objects.create(**task_fields)
		task_fields["task_name"] = ""
		form = TaskForm(data=task_fields)
		self.assertFalse(form.is_valid())
		self.assertTrue(form.errors)
		