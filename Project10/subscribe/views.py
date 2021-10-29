from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer
# Create your views here.

@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            data['response'] = "Nouvel utilisateur enregistré avec succès !"
            data['email'] = new_user.email
            data['first_name'] = new_user.first_name
            data['last_name'] = new_user.last_name
        else:
            print('ERROR DANS LA VALIDATION DU FORMULAIRE')
        return Response(data)
