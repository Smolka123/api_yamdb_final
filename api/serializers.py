from rest_framework import serializers

from .models import Category, Genre, Title, User


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


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title
