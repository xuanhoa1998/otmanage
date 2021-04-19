import transaction as transaction
from rest_framework import generics, permissions
from django.contrib.auth.models import User, UserManager
from employee.models import DBOTRequest, UserS
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


# login moi
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserS
#         fields = ('id', 'name', 'username', 'password', 'email', 'department')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     # def create(self):
#     #     employee = UserS.object.create(**self.validated_data)
#     #     return employee
#
#     def validate(self, attrs):
#         return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBOTRequest
        fields = ('id', 'employee', 'manager', 'title', 'description', 'date', 'start_time', 'end_time', 'approved')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")

    # class CustomRegisterSerializer(RegisterSerializer):
    #     gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    #     phone_number = serializers.CharField(max_length=30)

    # Define transaction.atomic to rollback the save operation in case of error
    # @transaction.atomic
    # def save(self, request):
    #     user = super().save(request)
    #     user.gender = self.data.get('gender')
    #     user.phone_number = self.data.get('phone_number')
    #     user.save()
    #     return user


# code moi