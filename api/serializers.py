from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'bio', 'email',
                  'role', 'confirmation_code']
        read_only_field = ('email', )


class ObtainingConfirmationCodeSerializer(serializers.ModelSerializer):
    """
    Sending confirmation code to the transmitted email.
    """
    class Meta:
        model = User
        fields = ('email', )


class TokenSerializer(serializers.Serializer):
    """
    Receiving a JWT token in exchange for email and confirmation code.
    """
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
