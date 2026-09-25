from django.urls import path
from todo_app.views import login, RegisterAPI, TasksAPI, is_completed, completed_tasks


urlpatterns = [
    path('login', login),
    path('register', RegisterAPI.as_view()),
    path('tasks', TasksAPI.as_view()),
    path('tasks/<int:task_id>', TasksAPI.as_view()),
    path('tasks/<int:task_id>/mark', is_completed),
    path('tasks/completed', completed_tasks)
]