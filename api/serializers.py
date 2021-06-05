from datetime import date

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
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

    def validate_year(self, year):
        """
        Checking the title's year is in the valid range
        """
        if year > date.today().year + 10 or year < -40000:
            message = f'the year {year} is outside the valid date range'
            raise serializers.ValidationError(message)
        return year


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title
