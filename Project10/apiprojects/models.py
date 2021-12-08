from django.db import models
from django.conf import settings
from django.db.models.fields import CharField, DateTimeField, IntegerField
# Create your models here.

class Project(models.Model):
    title = CharField(max_length=128)
    description = CharField(max_length=2048)
    type = CharField(max_length=64)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Contributors(models.Model):
    user = IntegerField()
    project = IntegerField()
    permission = CharField(max_length=256)
    role = CharField(max_length=256)

    def __str__(self):
        # To see the user's id and not the pk of the contributor's raw
        return f"{self.user}"

class Issue(models.Model):
    title = CharField(max_length=128)
    description = CharField(max_length=2048)
    tag = CharField(max_length=64)
    priority = CharField(max_length=64)
    state = CharField(max_length=64)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=Contributors, on_delete=models.CASCADE)
    created_time = DateTimeField(auto_now_add=True)

class Comment(models.Model):
    description = CharField(max_length=2048)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = DateTimeField(auto_now_add=True)
