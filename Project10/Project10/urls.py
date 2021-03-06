from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter as nested_router
from rest_framework_simplejwt import views as jwt_views
from apiprojects import views as api_views
from subscribe.views import registration_view

router = routers.SimpleRouter()
router.register('projects', api_views.ProjectViewSet, basename='project')

users_router = nested_router(router, 'projects', lookup='project')
users_router.register('users', api_views.ContributorViewSet, basename='contrib_users')

issues_router = nested_router(router, 'projects', lookup='project')
issues_router.register('issues', api_views.IssueViewSet, basename='issue')

comments_router = nested_router(issues_router, 'issues', lookup='issue')
comments_router.register('comments', api_views.CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', registration_view, name='register'),
]
