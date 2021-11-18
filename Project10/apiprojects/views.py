from django.http.response import HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.http import Http404
from .models import Project, Issue, Comment, Contributors
from .serializers import ContributorSerializer, ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user_info = {'id:': self.request.user.pk, 'email:':self.request.user.email,
                     'first_name:': self.request.user.first_name, 'last_name:': self.request.user.last_name}
        for key, value in user_info.items():
            print(key, value)
        return Project.objects.filter(author=self.request.user)

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
                user=self.request.user,
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
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request):
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

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
