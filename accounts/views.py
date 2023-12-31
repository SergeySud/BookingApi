from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import RegistrationSerializer


@authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered."
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)
