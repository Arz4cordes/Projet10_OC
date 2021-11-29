from django.http.response import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsProjectAuthor, IsProjectContributor, IsIssueAuthor, IsCommentAuthor
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Project, Issue, Comment, Contributors
from .serializers import ContributorSerializer, ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectAuthor]


    def get_queryset(self):
        user_contributions = Contributors.objects.filter(user=self.request.user.pk)
        user_projects = []
        for contribution in user_contributions:
            user_projects.append(contribution.project)
        return Project.objects.filter(id__in=user_projects)
    
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
            project_data = request.data
            new_project = Project.objects.create( 
            title=project_data['title'],
            description=project_data['description'],
            type=project_data['type'],
            author=self.request.user
            )
            new_project.save()
            new_contribution = Contributors.objects.create(
                user=self.request.user.pk,
                project=new_project.pk,
                permission='read, update, delete',
                role='author'
            )
            new_contribution.save()
            serializer = ProjectSerializer(new_project)
            return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).update(request, *args, **kwargs)


class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectContributor]


    def get_queryset(self, *args, **kwargs):
        return Contributors.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
            project_id = self.kwargs['project_pk']
            contribution_data = request.data
            new_contribution = Contributors.objects.create( 
            user=contribution_data['user'],
            permission='read',
            role='contributor',
            project=project_id
            )
            new_contribution.save()
            serializer = ContributorSerializer(new_contribution)
            return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        user_id = pk
        contribution = Contributors.objects.filter(project=project_id, user=user_id)
        contribution.delete()
        return HttpResponse('contributeur effacé...')



class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsIssueAuthor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project_ref = get_object_or_404(Project, pk=project_id)
        issue_data = request.data
        try:
            assignee_ref = int(issue_data['assignee'])
            contributors = Contributors.objects.filter(project=project_id)
            contributors_list = []
            for contributor in contributors:
                contributors_list.append(contributor.user)
            if assignee_ref in contributors_list:
                contributor_assignee =get_object_or_404(Contributors, project=project_id, user=assignee_ref)
                new_issue = Issue.objects.create(
                    title=issue_data['title'],
                    description=issue_data['description'],
                    tag=issue_data['tag'],
                    assignee=contributor_assignee,
                    author=self.request.user,
                    project=project_ref
                )
                new_issue.save()
                serializer = IssueSerializer(new_issue)
                return Response(serializer.data)
            else:
                text = 'Création invalide, la personne assignée au problème'
                text += ' doit être contributeur'
                return Response(text)
        except ValueError as e:
            print(e)
            text = "Merci d'entrer un numéro d'utilisateur (nombre entier)"
            return Response(text)

    def destroy(self, request, pk=None, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project_ref = get_object_or_404(Project, id=project_id)
        issue_id = pk
        issue = Issue.objects.filter(project=project_ref, id=issue_id)
        issue.delete()
        return HttpResponse('Issue effacée...')

    def update(self, request, pk=None, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project_ref = get_object_or_404(Project, id=project_id)
        issue_id = pk
        issue = get_object_or_404(Issue, id=issue_id, project=project_ref)
        issue_data = request.data
        issue.title=issue_data['title']
        issue.description=issue_data['description']
        issue.tag=issue_data['tag']
        try:
            assignee_ref = int(issue_data['assignee'])
            contributors = Contributors.objects.filter(project=project_id)
            contributors_list = []
            for contributor in contributors:
                contributors_list.append(contributor.user)
            if assignee_ref in contributors_list:
                contributor_assignee =get_object_or_404(Contributors, project=project_id, user=assignee_ref)
                issue.assignee = contributor_assignee
                print(issue.assignee)
        except ValueError as e:
            print(e)
            text = "Merci d'entrer un numéro d'utilisateur (nombre entier)"
            return Response(text)
        issue.save(update_fields=['title', 'description', 'tag', 'assignee'])
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

class CommentViewSet(ModelViewSet):
    """ attributes:
    description
    author (Foreignkey)
    issue (Foreignkey)
    created_time (auto)
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsCommentAuthor]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        issue_id = self.kwargs['issue_pk']
        issue_ref = get_object_or_404(Issue, pk=issue_id)
        comment_data = request.data
        new_comment = Comment.objects.create(
            description=comment_data['description'],
            author=self.request.user,
            issue=issue_ref
        )
        new_comment.save()
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        issue_id = self.kwargs['issue_pk']
        issue_ref = get_object_or_404(Issue, id=issue_id)
        comment_id = pk
        comment = Comment.objects.filter(id=comment_id, issue=issue_ref)
        comment.delete()
        return HttpResponse('Commentaire effacé...')

    def update(self, request, pk=None, *args, **kwargs):
        issue_id = self.kwargs['issue_pk']
        issue_ref = get_object_or_404(Issue, id=issue_id)
        comment_id = pk
        comment = get_object_or_404(Comment, id=comment_id, issue=issue_ref)
        comment_data= request.data
        comment.description = comment_data['description']
        comment.save(update_fields=['description'])
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
