from django.http.response import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsProjectAuthor, IsProjectContributor, IsIssueContributor, IsCommentContributor
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project, Issue, Comment, Contributors
from .serializers import ContributorSerializer, ProjectSerializer, IssueSerializer, CommentSerializer
from subscribe.models import User


class ProjectViewSet(ModelViewSet):
    """
    With this Class Based View, you can:
    Create a new project
    Read the list of projects for which the user autheticated is a contributor
    or read a particular project in same conditions
    Update or Delete a particular project
    if the user authenticated is the project's author
    To check if request.user is a project's author,
    the permission IsProjectAuthor is used
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectAuthor]


    def get_queryset(self):
        if self.action == 'retrieve':
            return Project.objects.all()
        else:
            user_contributions = Contributors.objects.filter(user=self.request.user.pk)
            user_projects = [contribution.project for contribution in user_contributions]
            return Project.objects.filter(id__in=user_projects)
  

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_contribution = Contributors.objects.create(
                user=request.user.pk,
                project=serializer.data["id"],
                permission='read, update, delete',
                role='author'
            )
        new_contribution.save()
        return Response(serializer.data)

            
    
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        project_id = pk
        project_to_delete = Project.objects.filter(pk=project_id)
        project_to_delete.delete()
        output_data = {'action effectuée:': 'projet effacé.'}
        return Response(output_data)


class ContributorViewSet(ModelViewSet):
    """
    With this Class Based View, you can:
    Create a new contributor for a project
    and Read the list of contributors for a particular project
    if the user authenticated is a project's contributor,
    Delete a contributor for a project
    if the user authenticated is the project's author.
    To check if request.user is a project's contributor,
    the permission IsProjectContributor is used
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsProjectContributor]


    def get_queryset(self, *args, **kwargs):
        return Contributors.objects.filter(project=self.kwargs['project_pk'])


    def create(self, request, *args, **kwargs):
            project_id = self.kwargs['project_pk']
            contribution_data = request.data
            try:
                # Here check if the new contributor is a user who exists
                contributor = User.objects.filter(pk=contribution_data['user'])
                data_constraints = contributor.exists()
                if data_constraints:
                    new_contribution = Contributors.objects.create( 
                    user=contribution_data['user'],
                    permission='read',
                    role='contributor',
                    project=project_id
                    )
                    new_contribution.save()
                    serializer = ContributorSerializer(new_contribution)
                    return Response(serializer.data)
                else:
                    text = "Cet utilisateur n'existe pas..."
                    return Response({'id utilisateur incorrect' : text})
            except ValueError as e:
                print(e)
                text = "Merci d'entrer un numéro d'utilisateur (nombre entier) pour assignee"
                output_data = {'création invalide': text}
                return Response(output_data)


    def destroy(self, request, pk=None, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        user_id = pk
        contribution = Contributors.objects.filter(project=project_id, user=user_id)
        contribution.delete()
        output_data = {'action effectuée:': 'contributeur effacé.'}
        return Response(output_data)



class IssueViewSet(ModelViewSet):
    """
    With this Class Based View, you can:
    Create a new issue
    and Read the list of issues for a particular project
    if the user authenticated is a project's contributor,
    Update or Delete a particular issue
    if the user authenticated is the issue's author
    To check if request.user is a project's contributor
    or if request.user is the issue's author,
    the permission IsIssueContributor is used
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsIssueContributor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """
        get back the project's id and some attributes sent in the request,
        check if the assignee sent in the post request
        is a project's contributor,
        create a new Issues object with the attribute author = request.user,
        and save the new issue in the database
        """
        project_id = self.kwargs['project_pk']
        contributors = Contributors.objects.filter(project=project_id)
        contributors_list = [str(contributor.user) for contributor in contributors]
        constraint = request.data['assignee'] in contributors_list
        if not constraint:
            return Response({'Erreur de saisie': 'assignee doit être un contributeur'})
        else:
            contributor = get_object_or_404(Contributors, project=project_id, 
                                            user=request.data['assignee'])
            request.POST._mutable = True
            request.data["project"] = project_id
            request.data["assignee"] = contributor.pk
            request.data["author"] = request.user.pk
            request.POST._mutable = False
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
           

    def destroy(self, request, pk=None, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        project_ref = get_object_or_404(Project, id=project_id)
        issue_id = pk
        issue = Issue.objects.filter(project=project_ref, id=issue_id)
        issue.delete()
        return HttpResponse('Issue effacée...')

    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_pk']
        contributors = Contributors.objects.filter(project=project_id)
        contributors_list = [str(contributor.user) for contributor in contributors]
        constraint = request.data['assignee'] in contributors_list
        if not constraint:
            return Response({'Erreur de saisie': 'assignee doit être un contributeur'})
        else:
            contributor = get_object_or_404(Contributors, project=project_id, 
                                            user=request.data['assignee'])
            request.POST._mutable = True
            request.data["project"] = project_id
            request.data["assignee"] = contributor.pk
            request.data["author"] = request.user.pk
            request.POST._mutable = False
            return super(IssueViewSet, self).update(request, *args, **kwargs)

class CommentViewSet(ModelViewSet):
    """
    With this Class Based View, you can:
    Create a new comment
    and Read the list of comments for a particular issue
    if the user authenticated is the project's contributor,
    Update or Delete a particular comment
    if the user authenticated is the comment's author
    To check if request.user is the project's contributor
    or if request.user is the comment's author,
    the permission IsCommentContributor is used
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsCommentContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """
        get back the issue's id and some attributes sent in the request,
        create a new Comment object with the attribute author = request.user,
        and save the new comment in the database
        """
        issue_id = self.kwargs['issue_pk']
        request.POST._mutable = True
        request.data["issue"] = issue_id
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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
        request.POST._mutable = True
        request.data["issue"] = issue_id
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).update(request, *args, **kwargs)
