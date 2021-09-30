# coding=utf-8
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SlugRelatedField
from rest_framework.serializers import ValidationError

from api.models import Category
from api.models import Comment
from api.models import Genre
from api.models import Review
from api.models import Title


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
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


class RepresentationField(SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class TitleSerializer(ModelSerializer):
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
    rating = IntegerField(read_only=True)
