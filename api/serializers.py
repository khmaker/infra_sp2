from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField, \
    ValidationError

from .models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre
        lookup_field = 'slug'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category
        lookup_field = 'slug'


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == 'POST':
            if Review.objects.filter(
                    title=self.context.get('view').kwargs.get('title_id'),
                    author=request.user).exists():
                raise ValidationError('Review already exists')
        return attrs


class RepresentationField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class TitleSerializer(serializers.ModelSerializer):
    category = RepresentationField(slug_field='slug',
                                   queryset=Category.objects.all()
                                   )
    genre = RepresentationField(slug_field='slug',
                                queryset=Genre.objects.all(),
                                many=True
                                )

    class Meta:
        fields = '__all__'
        model = Title


class TitleListRetrieveSerializer(TitleSerializer):
    rating = serializers.IntegerField(read_only=True)
