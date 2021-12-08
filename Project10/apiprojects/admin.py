from django.contrib import admin
from .models import Project, Comment, Issue, Contributors

# Register your models here.

admin.site.register(Project)
admin.site.register(Contributors)
admin.site.register(Issue)
admin.site.register(Comment)