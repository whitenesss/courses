from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from cours.views import SubscriptionCreateAPIView
from users.apps import UsersConfig
from users.views import UserCreateRetrieveUpdateDestroyAPIView

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'', UserCreateRetrieveUpdateDestroyAPIView, basename='user')
urlpatterns = [

    path("token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("", include(router.urls)),

]
