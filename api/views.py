import uuid

from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin
from api.serializers import (UserSerializer,
                             ObtainingConfirmationCodeSerializer,
                             TokenSerializer)
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin, )
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ('username', )

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated, ),
            url_name='me', url_path='me')
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=instance.email, role=instance.role)
        return Response(serializer.data, status=200)


class ObtainingConfirmationCodeView(APIView):
    """Processing a request to receive a code,
    sending it to the email specified by the user during registration.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ObtainingConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            confirmation_code = uuid.uuid4()
            User.objects.get_or_create(email=email,
                                       username=str(email),
                                       confirmation_code=confirmation_code,
                                       is_active=False)
            send_mail(
                'Confirmation Code',
                f'confirmation_code: {confirmation_code}',
                'yamdb@yamdb.ru',
                [email],
                fail_silently=False,
            )
            return Response(
                {'result': f'Confirmation Code отправлен на {email}'},
                status=200
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """
    Handling a request to get(method-post) or refresh the user's JWT token
    """
    permission_classes = (AllowAny, )

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        user.save()
        refresh_token = RefreshToken.for_user(user)
        return Response({'token': str(refresh_token.access_token)})
