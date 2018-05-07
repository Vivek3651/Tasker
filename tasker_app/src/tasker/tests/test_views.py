from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ..models import Task, TaskManager
# Create your tests here.

class UserSignUpTestCase(TestCase):
	def test_user_signUp(self):
		response = self.client.get(reverse("user_signup"))
		self.assertEqual(response.status_code, 200)

class LoginViewTestCase(TestCase):
	def test_login_view(self):
		task_list_url = reverse("login")
		response = self.client.get(task_list_url)
		self.assertEqual(response.status_code, 200)

class TaskViewTestCases(TestCase):
	def setUp(self):
		self.client = Client()
		user_fields = {
			"username":"Mike",
			"email":"mike@gamil.com",
			"password":"pass"
		}
		self.user = User.objects.create_user(**user_fields)

	def test_login(self):
		task_list_url = reverse("task_list")
		response = self.client.get(task_list_url)
		# user is not logged in
		self.assertEqual(response.status_code, 302)

	def test_task_list_view(self):
		self.client.login(username='Mike', password='pass')
		response = self.client.get(reverse("task_list"))
		self.assertEqual(response.status_code, 200)

	def test_task_create_view(self):
		self.client.login(username='Mike', password='pass')
		response = self.client.get(reverse("task_create"))
		self.assertEqual(response.status_code, 200)

class TaskUpdateTestCase(TestCase):

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

		self.task_manager_obj = TaskManager.objects.create(**task_manager_fields)

	def test_task_update_view(self):
		self.client.login(username='Mike', password='pass')
		response = self.client.get(reverse("task_update", kwargs={"pk":self.task_manager_obj.id}))
		self.assertEqual(response.status_code, 302)
