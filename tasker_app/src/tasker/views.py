from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from tasker.forms import UserSignUpForm, TaskForm, TaskManagerForm, UserListForm
from tasker.models import TaskManager, Task

# Create your views here.
@login_required
def task_list(request):
	
	status = request.GET.get('status')
	task_list = TaskManager.objects.all()
	if status == "active":
		task_list = task_list.filter(task_status=TaskManager.UNDONE)
	
	task_list.order_by("timestamp")
	users_list_form = UserListForm()
	
	completed_task_list = TaskManager.objects.filter(
		task_status=TaskManager.DONE)
	context = {'task_list':task_list, 
	'completed_task_list':completed_task_list,
	'status':status, 'users_list_form':users_list_form}

	return render(request,'tasker/task_list_page.html', context)


def login_view(request):
	return render(request,'tasker/login.html')

def logout_view(request):
    logout(request)
    # Redirect to a success page.

def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('task_list')
    else:
    	form = UserSignUpForm()
    return render(request, 'tasker/user_signup.html', {'form': form})

@login_required
def create_task(request):
	task_form = TaskForm()
	task_manager_form = TaskManagerForm()
	success = False
	if request.method == 'POST':
		
		task_form = TaskForm(request.POST)
		task_manager_form = TaskManagerForm(request.POST)
		task_owner = request.user

		if task_manager_form.is_valid():
		    task_manager_form = task_manager_form.save(commit=False)
		    task_manager_form.task_owner = task_owner
		    task_manager_form.save()
		    success = True

		elif task_form.is_valid():
			task_obj = task_form.save()
			TaskManager.objects.create(task=task_obj,
				task_owner=task_owner)
			success = True

		if success:
			return redirect('task_list')

	context = {'task_form': task_form, 'task_manager_form':task_manager_form}
	return render(request, 'tasker/task_create.html', context)

class DeleteTask(DeleteView):
    model = TaskManager
    success_url = reverse_lazy('task_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.task_owner:
        	self.object.delete()
        return HttpResponseRedirect(self.success_url)

@login_required
def mark_task_as_done(request, pk):
	status = request.GET.get('status')
	task_manager = TaskManager.objects.get(id=pk)
	user_id = None
	if request.user != task_manager.task_owner:
		return redirect('task_list')

	user_form = UserListForm(request.POST)
	if user_form.is_valid():
		user_id =  user_form.cleaned_data.get("user")

	if status == "done":
		task_manager.task_status = TaskManager.DONE
		task_manager.completed_by = user_id

	elif status == "undone":
		task_manager.task_status = TaskManager.UNDONE
		task_manager.completed_by = None
	
	task_manager.save()
	return redirect('task_list')

@login_required
def task_edit(request, pk):
    """
    Function for updating the Task
    """
    task_manager = TaskManager.objects.get(id=pk)
    task = task_manager.task
    if request.method == 'POST':
    	task_form = TaskForm(request.POST)
    	task_owner = request.user

    	if task_form.is_valid():
    		task_name = task_form.cleaned_data.get('task_name')
    		task_description = task_form.cleaned_data.get('task_description')

    		if task_manager.task_owner == task_owner:
    			task.task_name = task_name
    			task.task_description = task_description
    			task.save()
    			return redirect('task_list')
    else:
    	form = TaskForm(instance=task)

    context = {'form': form, 'task_manager':task_manager}
    return render(request, 'tasker/task_edit.html', context)