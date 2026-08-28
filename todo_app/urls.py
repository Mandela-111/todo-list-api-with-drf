from django.urls import path
from todo_app.views import login, register


urlpatterns = [
    path('login', login),
    path('register', register)
]