from rest_framework import serializers
from .models import Contributors, Project, Issue, Comment
from subscribe.models import User
from django.shortcuts import get_object_or_404

 
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_id']



class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user', 'project', 'permission', 'role']


class IssueSerializer(serializers.ModelSerializer):
    assignee = serializers.StringRelatedField(many=False)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'state', 'project', 'author', 'assignee', 'created_time']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
