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

"""
class subscription(FormView):
    template_name = 'subscribe/new_user.html'
    form_class = UserForm
    success_url = reverse_lazy('login_page')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # form.save() OU BIEN FAIRE
            # email = request.POST['email']
            # first_name = request.POST['first_name']
            # last_name = request.POST['last_name']
            # password = request.POST['password']
            # PUIS
            # méthode créate_user(email, first_name, last_name, password) ? 
            return redirect('subscribe:login_page')
        return render(request, self.template_name, {'form': form})
"""


