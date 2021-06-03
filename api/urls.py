from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories-list'
)
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres-list'
)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles-list'
)

urlpatterns = [
    path('v1/',
         include(v1_router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
