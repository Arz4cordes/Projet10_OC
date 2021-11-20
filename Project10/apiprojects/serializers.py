from rest_framework import serializers
from .models import Contributors, Project, Issue, Comment
 
 
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_id']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user', 'project', 'permission', 'role']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'project', 'author', 'assignee', 'created_time']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
