from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tasker.models import TaskManager, Task
from django.forms import ModelForm

class UserSignUpForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class TaskManagerForm(ModelForm):

	class Meta:
		model = TaskManager
		fields = ['task']

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['task_name', 'task_description']

class UserListForm(forms.Form):
	user_list = User.objects.all()
	user = forms.ModelChoiceField(queryset=user_list, required=False, label='Task completed by:')