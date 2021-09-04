
from account_management.views import DecoratedTokenVerifyView, UserAccountManagerViewSet
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

user_account_get_post_patch_delete = UserAccountManagerViewSet.as_view(
    {
        "get": "retrieve",
        "post": "create",
        "patch": "update",
        "delete": "destroy"
    }
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path("user_account/", user_account_get_post_patch_delete),
    path('token/verify/',
         TokenVerifyView.as_view(), name='token_verify'),
]
