# coding=utf-8
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.models import Category
from api.models import Genre
from api.models import Review
from api.models import Title
from api.serializers import CategorySerializer
from api.serializers import CommentSerializer
from api.serializers import GenreSerializer
from api.serializers import ReviewSerializer
from api.serializers import TitleListRetrieveSerializer
from api.serializers import TitleSerializer
from users.permissions import IsAdminOrReadOnly
from users.permissions import IsStaffOrAuthorOrReadOnly


class GenreViewSet(
        CreateModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        GenericViewSet
        ):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete')


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
            )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
            )
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(
        CreateModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        ListModelMixin,
        GenericViewSet
        ):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete')


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListRetrieveSerializer
        return super().get_serializer_class()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        return Review.objects.filter(title__id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save()
