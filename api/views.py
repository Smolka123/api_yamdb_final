from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


from api.permissions import IsAdmin
from api.serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ('username', )

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated, ), url_path='me')
    def me(self, request, *args, **kwargs):
        self.kwargs['username'] = self.request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        return self.update(request, partial=True)


    # @action(detail=False, methods=['get', 'patch'],
    #         permission_classes=(IsAuthenticated, ), url_path='me')
    # def me(self, request, *args, **kwargs):
    #     self.kwargs['username'] = self.request.user.username
    #     if request.method == 'GET':
    #         return self.retrieve(request)
    #     if request.method == 'PATCH':
    #         return self.update(request, partial=True)


    # def me(self, request):
    #     user = self.request.user
    #     serializer = self.get_serializer(user)
    #     if self.request.method == 'PATCH':
    #         serializer = self.get_serializer(user,
    #                                          data=request.data,
    #                                          partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #     return Response(serializer.data)
