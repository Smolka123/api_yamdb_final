from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CategoriesViewSet, GenresViewSet

v1_router = DefaultRouter()
v1_router.register(
    'categories',
    CategoriesViewSet,
    basename='categories-list'
)
v1_router.register(
    'genres',
    GenresViewSet,
    basename='genres-list'
)

urlpatterns = [
    path('v1/',
         include(v1_router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
