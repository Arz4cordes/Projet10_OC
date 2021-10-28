from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import AuthenticationForm

# urls pour la page d'accueil home_page qui permet de se connecter,
# la page subscribe avec le formulaire d'inscription,
# et le chemin vers l'application bookViewpoints avec les différentes autres vues
app_name = 'subscribe'


# créer sa propre vue connection avec la condition is_authenticate
urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(template_name='subscribe/login.html', authentication_form=AuthenticationForm),
         name='login_page'),
    path('subscribe/', views.subscription.as_view(), name='subscribe'),
    path('logout/', auth_views.LogoutView.as_view(template_name='subscribe/logout.html'), name='logout_page'),
]
