from rest_framework import serializers
from api.models import ManagerUser



class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for ManagerUser
    """

    class Meta:
        model = ManagerUser
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