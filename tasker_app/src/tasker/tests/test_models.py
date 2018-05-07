from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task, TaskManager
# Create your tests here.

class TaskModelTestCase(TestCase):
	def setUp(self):
		task_fields = {
			"task_name":"random",
			"task_description":"description",
		}
		Task.objects.create(**task_fields)
	def test_task_name(self):
		obj = Task.objects.get(task_name="random")
		self.assertEqual(obj.task_name, "random")

	def test_description_(self):
		obj = Task.objects.get(task_description="description")
		self.assertEqual(obj.task_description, "description")

class TaskManagerModelTestCase(TestCase):
	
	def setUp(self):
		task_fields = {
			"task_name":"random",
			"task_description":"description",
		}
		
		self.task_obj = Task.objects.create(**task_fields)
		
		user_fields = {
			"username":"Mike",
			"email":"mike@gamil.com",
			"password":"pass"
		}
		
		self.user = User.objects.create_user(**user_fields)

		task_manager_fields = {
			"task":self.task_obj,
			"task_owner":self.user,
			"task_status":TaskManager.UNDONE,
		}

		TaskManager.objects.create(**task_manager_fields)

	def test_task_manager_task(self):
		obj = TaskManager.objects.get(task=self.task_obj, task_owner=self.user)
		self.assertEqual(obj.task_status, TaskManager.UNDONE)
	
	def test_task_manager_task_status(self):
		obj = TaskManager.objects.get(task=self.task_obj, task_owner=self.user)
		self.assertEqual(obj.task_status, TaskManager.UNDONE)

	def test_task_manager_task_owner(self):
		obj = TaskManager.objects.get(task=self.task_obj, task_owner=self.user)
		self.assertEqual(obj.task_owner, self.user)

	def test_task_manager_task_completed_by(self):
		obj = TaskManager.objects.get(task=self.task_obj, task_owner=self.user)
		self.assertTrue(obj.completed_by == None)




