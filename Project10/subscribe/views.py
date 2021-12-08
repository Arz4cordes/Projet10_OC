
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from subscribe.serializers import UserRegistrationSerializer


@api_view(['POST',])
@authentication_classes(())
@permission_classes(())
def registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        new_user = serializer.save()
        data['response'] = 'Nouvel utilisateur enregistré avec succès !'
        data['email'] = new_user.email
        data['first_name'] = new_user.first_name
        data['last_name'] = new_user.last_name
        data['votre identifiant (notez le bien !)'] = new_user.pk
    else:
        print('ERREUR DANS LA VALIDATION DU FORMULAIRE')
    return Response(data)
