from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors, Issue, Project, Comment
# IsAuthenticated est déjà géré par le framework


class IsProjectAuthor(BasePermission):
    """
    permission qui vérifie si request.user est l'auteur du projet,
    pour modifier ou effacer un projet / pour effacer un contributeur
    """
    
    def has_permission(self, request, view):
        print(request.user.has_perm('apiprojects.view_project'))
        if request.method in ["POST", "GET"]:
            return True
        else:
            project = Project.objects.filter(pk=view.kwargs["pk"],
                                             author=request.user)
            return project.exists()

    def has_object_permission(self, request, view, obj):
        user_contributions = Contributors.objects.filter(user=request.user.pk)
        user_projects = [contribution.project for contribution in user_contributions]
        return obj.pk in user_projects


class IsProjectContributor(BaseException):
    """
    permission qui vérifie si request.user est un contributeur du projet,
    pour voir ou ajouter un contributeur,
    voir le projet,
    créer une issue,
    ou créer un commentaire sur une issue
    """
    def has_permission(self, request, view):
        contributors = Contributors.objects.filter(user=request.user.pk,
                                                   project=view.kwargs['project_pk'])
        if request.method in ["GET", "POST"]:
            return contributors.exists()
        else:
            project = Project.objects.filter(pk=view.kwargs['project_pk'],
                                             author=request.user)
        return contributors.exists() and project.exists()


class IsIssueContributor(BasePermission):
    """
    permission qui vérifie si request.user est l'auteur d'une issue,
    pour modifier ou supprimer une issue
    """
    def has_permission(self, request, view):
        contributors = Contributors.objects.filter(user=request.user.pk,
                                                   project=view.kwargs['project_pk'])
        if request.method in ['GET', 'POST']:
            return contributors.exists()
        else:
            issue = Issue.objects.filter(pk=view.kwargs['pk'],
                                         author=request.user)
            return issue.exists() and contributors.exists()

class IsCommentContributor(BasePermission):
    """
    permission qui vérifie si request.user est l'auteur d'un commentaire,
    pour modifier ou supprimer un commentaire
    """
    def has_permission(self, request, view):
        contributors = Contributors.objects.filter(user=request.user.pk,
                                                   project=view.kwargs['project_pk'])
        if request.method in ['GET', 'POST']:
            return contributors.exists()
        else:
            comment = Comment.objects.filter(pk=view.kwargs['pk'],
                                             author=request.user)
            return comment.exists() and contributors.exists()
