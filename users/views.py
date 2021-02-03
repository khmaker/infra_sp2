from django.contrib.auth.tokens import default_token_generator as dtg
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrSuperUser
from .serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrSuperUser)

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me')
    def get_me(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_me.mapping.patch
    def patch_me(self, request):
        serializer = UserSerializer(self.request.user,
                                    data=self.request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreateUserAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (AnonRateThrottle,)
    http_method_names = ('post',)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=serializer.validated_data.get('email'))
        user = serializer.instance
        user.email_user(subject='Confirmation_code for yamdb',
                        message=dtg.make_token(user))
        return Response(data='Check your mail', status=status.HTTP_201_CREATED)


class GetTokenAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (AnonRateThrottle,)
    http_method_names = ('post',)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        if dtg.make_token(user) != request.data.get('confirmation_code'):
            return Response(data='Invalid Confirmation_code',
                            status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response(data={'token': str(refresh.access_token)},
                        status=status.HTTP_201_CREATED)
