from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import RegistrationSerializer


# Create your views here.
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        serializer_class = RegistrationSerializer(data=request.data)
        data = {}
        if serializer_class.is_valid():
            account = serializer_class.save()
            data['response'] = "Successfully registered."
            data['username'] = account.username
        else:
            data = serializer_class.errors
        return Response(data)