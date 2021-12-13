from rest_framework import serializers
from .models import Contributors, Project, Issue, Comment

 
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author']

    def get_fields(self):
        fields = super(ProjectSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields



class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user', 'project', 'permission', 'role']

    def get_fields(self):
        fields = super(ContributorSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'state', 'assignee', 'created_time', 'project', 'author']

    def get_fields(self):
        fields = super(IssueSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields
