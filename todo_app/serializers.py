from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import Serializer, ValidationError, ModelSerializer


# TODO: create RegisterSerializer(inheriting from User model); validate username and password. Validate password??

class RegisterSerializer(ModelSerializer):

    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }

    def validate_confirm_password(self, value):

        password = self.initial_data.get('password')

        if password != value:
                raise ValidationError({"confirm_password": "Passwords do not match"})

        return value

    def validate_username(self, value):

        username = "".join(value.split()).lower()

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken.")

        return username



    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already in use.")
        return email



    def create(self, validated_data):
        validated_data.pop('confirm_password', None) # for safety

        return User.objects.create_user(**validated_data)



class LoginSerializer(Serializer):
    #  what would the login serializer need? the username and password because
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, allow_blank=False)



    def validate(self, data) :

        if len(self.initial_data) > 2:
            raise ValidationError("Payload contains too many items. Only username and password are allowed.")

        username = data.get('username').lower()
        username = "".join(username.split())
        print(username)
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise ValidationError("Email or password is invalid")

            if not user.is_active:
                raise ValidationError("This user account is inactive.")

            data['user'] = user
            return data

        raise ValidationError("Must include username and password")


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']