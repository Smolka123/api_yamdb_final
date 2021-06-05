import uuid

from django.core.mail import send_mail
from django.db.models.aggregates import Avg
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Genre, Title, Review, User
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          ObtainingConfirmationCodeSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer,CommentSerializer,
                          ReviewSerializer)

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsAuthorOrStaffOrReadOnly



class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug',)
    category = filters.CharFilter(field_name='category__slug',)
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='year')


class BaseModelViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    pass


class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [SearchFilter]
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(BaseModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [SearchFilter]
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin, )
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = [SearchFilter]
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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id',))
        return review.comments.all()


    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.kwargs.get('review_id',),
                        title_id=self.kwargs.get('title_id',))


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly)
    

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
        self.get_rank(title)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.reviews.all()
        return queryset

    def get_rank(self, title):
        rank = self.get_queryset().aggregate(Avg('score'))
        title.rank = round(rank['score__avg'], 2)
        title.save(update_fields=['rank'])
