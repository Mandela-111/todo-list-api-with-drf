from django.urls import path
from todo_app.views import login, RegisterAPI


urlpatterns = [
    path('login', login),
    path('register', RegisterAPI.as_view())
]