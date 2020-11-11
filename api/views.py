from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView

from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from api.models import ManagerUser
from api import serializers
from api import models


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



class PlansListView(generics.ListAPIView):
    """
    List all plans
    """
    queryset = models.Plan.objects.all()
    serializer_class = serializers.PlanSerializer


class PlanCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.PlanSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            plan = serializer.create(serializer.data)
            return Response({"id":plan.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreditCardView(APIView):
    """
    Credit Card View
    """
    
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        user = self.request.user
        return user
    
    def get(self, request, *args, **kwargs):
        try:
            card = models.CreditCard.objects.get(user=self.get_object())
            serializer = serializers.CreditCardSerializer(card, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.CreditCard.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        request.data["user"] = user.id
        serializer = serializers.CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            instance, created = serializer.get_or_create()
            if not created:
                serializer.update(instance, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        user = request.user
        request.data["user"] = user.id
        card = models.CreditCard.objects.get(user=user)
        serializer = serializers.CreditCardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
