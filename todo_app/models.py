from django.db import models
from django.contrib.auth.models import User
from utils.models import TimeStampedModel



# Create your models here.
class Tasks(TimeStampedModel):
    title, description, isCompleted = models.CharField(default='Title', max_length=50), models.CharField(), models.BooleanField()
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')


