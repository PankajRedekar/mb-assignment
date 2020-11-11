from datetime import date, datetime
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import fields
from api import models



class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for ManagerUser
    """

    class Meta:
        model = models.ManagerUser
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class SignupSerializer(serializers.Serializer):
    """
    SignUp serializer.
    Validates Signup request data.
    """

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    password1 = serializers.CharField(max_length=200)

    def is_valid(self):
        valid = super(SignupSerializer, self).is_valid()
        if not valid:
            return valid
        
        #confirm password and password1 are same
        valid = self.data["password"] == self.data["password1"]
        if not valid:
            raise serializers.ValidationError("passowrd mismatch. password and password1 should be same")
        
        del self.data["password1"]
        return valid



class ChangePasswordSerializer(serializers.Serializer):
    """
    Change Password serilizer.
    Validates password change data.
    """
    old_password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200)

    def is_valid(self):
        valid = super(ChangePasswordSerializer, self).is_valid()
        if not valid:
            return valid
        
        #confirm new password and confirm password are same
        valid = self.data["new_password"] == self.data["confirm_password"]
        if not valid:
            raise serializers.ValidationError(["passowrd mismatch. new_password and confirm_password should be same"])

        return valid



class PlanSerializer(serializers.ModelSerializer):
    """
    Serializer for Plan model
    """

    class Meta:
        model = models.Plan
        fields = ('title', 'validity', 'price', 'description')

    def create(self, validated_data):
        plan = models.Plan(
            title=validated_data["title"],
            validity=validated_data["validity"],
            price=validated_data["price"],
            description=validated_data["description"]
        )
        plan.save()
        return plan



class SubsciptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Subscription model
    """
    start_date = fields.DateField(input_formats=['%Y-%m-%d'])
    expiry_date = fields.DateField(input_formats=['%Y-%m-%d'])
    
    class Meta:
        model = models.Subscription
        fields = '__all__'




class CreditCardSerializer(serializers.ModelSerializer):
    """
    Credit Card serializer
    """
    expiry_date = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = models.CreditCard
        exclude = ('cvv','user')

    def is_valid(self):
        valid = super(CreditCardSerializer, self).is_valid()
        if not valid:
            return valid
        if self.validated_data["expiry_date"] < date.today():
            raise serializers.ValidationError({"expiry_date":"The date cannot be in the past!"})

        return True


    def get_or_create(self):
        return models.CreditCard.objects.get_or_create(defaults=self.validated_data)