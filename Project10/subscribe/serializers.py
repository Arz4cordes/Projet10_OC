from rest_framework import serializers
from subscribe.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
 
 
    def save(self):
        new_user = User.objects.create_user(email = self.validated_data['email'],
        first_name = self.validated_data['first_name'],
        last_name = self.validated_data['last_name'],
        password = self.validated_data['password'])
        return new_user
