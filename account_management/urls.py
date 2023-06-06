from account_management.views import (
    DecoratedTokenVerifyView,
    UserAccountManagerViewSet,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
)
from django.urls import path


user_account_get_post_patch_delete = UserAccountManagerViewSet.as_view(
    {"get": "retrieve", "post": "create", "patch": "update", "delete": "destroy"}
)


urlpatterns = [
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("user_account/", user_account_get_post_patch_delete, name="user_crud"),
    path(
        "search_user/",
        UserAccountManagerViewSet.as_view({"get": "search_user"}),
        name="search_user",
    ),
    path("token/verify/", DecoratedTokenVerifyView.as_view(), name="token_verify"),
]
