from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.task_list, name='task_list'),
    url(r'^user/signup/$', views.user_signup, name='user_signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'login'}, name='logout'),
    url(r'^create/task/$', views.create_task, name='task_create'),
    url(r'^task/delete/(?P<pk>\d+)/delete/$', login_required(views.DeleteTask.as_view()),
        name='task_delete'),
    url(r'^task/(?P<pk>\d+)/update/$', views.mark_task_as_done, name='task_update'),
    url(r'^task/(?P<pk>\d+)/edit/$', views.task_edit, name='task_edit_url'),
]