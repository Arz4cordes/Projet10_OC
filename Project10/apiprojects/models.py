from django.db import models
from django.conf import settings
from django.db.models.fields import CharField, DateTimeField, IntegerField
# Create your models here.

class Projects(models.Model):
    title = CharField(max_length=128)
    description = CharField(max_length=2048)
    p_type = CharField(max_length=64)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Issues(models.Model):
    title = CharField(max_length=128)
    description = CharField(max_length=2048)
    tag = CharField(max_length=64)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = DateTimeField(auto_now_add=True)

class Comments(models.Model):
    description = CharField(max_length=2048)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = DateTimeField(auto_now_add=True)

class Contributors(models.Model):
    user_id = IntegerField()
    project_id = IntegerField()
    permission = CharField(max_length=256)
    role = CharField(max_length=256)
