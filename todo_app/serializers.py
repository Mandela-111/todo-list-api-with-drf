from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import Serializer, ValidationError


class LoginSerializer(Serializer):
    #  what would the login serializer need? the username and password because
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, allow_blank=False)
    #   there's no need to save to the database. After the fields, it then needs
    #   to be authenticated to confirm if the user exists.


    def validate(self, data) :

        if len(self.initial_data) > 2:
            raise ValidationError("Payload contains too many items. Only username and password are allowed.")

        # we get the username and password from the data that's passed and authenticate it
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


class UserListSerializer(serializers.Serializer):
    model = User
    fields = ['username', 'email']