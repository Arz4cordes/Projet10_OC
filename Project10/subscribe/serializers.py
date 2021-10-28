from rest_framework import serializers

from django.contrib.auth import get_user_model

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
       

    def save(self):
        new_user = get_user_model(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Les mots de passes ne correspondent pas'})
        new_user.set_password(password)
        new_user.save()
        return new_user
