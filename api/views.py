from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics

from django.db.utils import IntegrityError

from api.models import ManagerUser
from api import serializers

class ManagerUserListView(generics.ListAPIView):
    """
    List of ManagerUser API
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ManagerUser.objects.all()
    serializer_class = serializers.UserSerializer


class ManagerUserCreateView(generics.CreateAPIView):
    """
    Create ManagerUser API
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SignupSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.data
                del data['password1']
                u = ManagerUser.objects.create_user(**data)
                return Response({"id":u.id}, status=status.HTTP_201_CREATED)
            except IntegrityError as i:
                return Response({"error":str(i)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change Password API
    """
    model = ManagerUser
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
                # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                    'user': self.object.email,
                    'message': 'Password updated successfully'
                }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
