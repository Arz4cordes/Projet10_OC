from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from apiprojects import views as api_views
from subscribe.views import registration_view

router = routers.SimpleRouter()
router.register('project', api_views.ProjectViewSet, basename='project')
router.register('issue', api_views.IssueViewSet, basename='issue')
router.register('comment', api_views.CommentViewSet, basename='comment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register', registration_view, name='register'),
]
