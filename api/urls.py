from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from api.views import UserViewSet, ObtainingConfirmationCodeView, TokenView

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)


urlpatterns = [
    path('v1/',
         include(v1_router.urls)),
    path('v1/auth/email/',
         ObtainingConfirmationCodeView.as_view(),
         name='conformation_code'),
    path('v1/auth/token/',
         TokenView.as_view(),
         name='token'),
    path('v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
