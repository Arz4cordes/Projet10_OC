from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name',
                  'email', 'password']
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Adresse mail valide (servira d'identifiant)",
            "password": "Mot de passe"
        }

class AuthenticationForm(AuthenticationForm):
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            print("Le compte existe, mais il est inactif.")