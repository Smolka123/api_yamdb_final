from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Comments, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments
        #read_only_fields = ['author', 'pub_date']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='id'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


    def validate(self, data):
        title = get_object_or_404(Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if (Review.objects.filter(title=title,
                                  author=author,).exists() and 
                                  self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Нельзя публиковать больше одного отзыва на тайтл'
            )
        return data