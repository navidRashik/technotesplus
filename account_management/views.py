import logging
import uuid

from django.contrib.auth.hashers import make_password
from django.db.models.query_utils import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.response import Response
from account_management.models import UserAccount
from utils.response_wrapper import ResponseFormatSerializer, ResponseWrapper

from .serializers import (
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
    UserAccountPatchSerializer,
    UserAccountSerializer,
    UserSignupSerializer,
)

logger = logging.getLogger(__name__)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseFormatSerializer(
                TokenObtainPairResponseSerializer
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseFormatSerializer(TokenRefreshResponseSerializer)
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseFormatSerializer(TokenVerifyResponseSerializer)
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserAccountManagerViewSet(viewsets.ModelViewSet):
    # logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """

        if self.action == "create":
            self.serializer_class = UserSignupSerializer
        elif self.action == "update":
            self.serializer_class = UserAccountPatchSerializer
        # elif self.action == "get_otp":

        #     self.serializer_class = None
        else:
            self.serializer_class = UserAccountSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        elif self.action in ["retrieve", "search_user"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            # permissions.DjangoObjectPermissions.has_permission()
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = UserAccount.objects.exclude(status="DEL")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            password = serializer.validated_data.pop("password")
            username = serializer.validated_data.pop("username")
        except Exception as e:
            return Response(data=e.args, status=401, exception=True)
        try:
            username_exist = UserAccount.objects.filter(username=username).exists()
            if username_exist:
                return Response(
                    data="Please use different username, it’s already been in use",
                    status=400,
                    exception=True,
                )
            password = make_password(password=password)
            user = UserAccount.objects.create_user(
                username=username, password=password, **serializer.validated_data
            )
            # user = UserAccount.objects.create(password=password, **request.data)
        except Exception as e:
            logger.error("Account creation failed", e.args)
            return Response(data="Account creation failed", status=401, exception=True)

        user_serializer = UserAccountSerializer(instance=user, many=False)
        return Response(data=user_serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        password = request.data.pop("password", None)
        user_qs = UserAccount.objects.filter(pk=request.user.pk)
        request.data.get("first_name")
        request.data.get("last_name")

        # if user_qs:
        if password:
            password = make_password(password=password)
            updated = user_qs.update(password=password, **request.data)
        else:
            updated = user_qs.update(**request.data)
        if not updated:
            return ResponseWrapper(
                error_code=status.HTTP_400_BAD_REQUEST, error_msg=["failed to update"]
            )
        # is_apps = request.path.__contains__('/apps/')

        user_serializer = UserAccountSerializer(instance=user_qs.first(), many=False)
        return ResponseWrapper(data=user_serializer.data, status=200)

    def retrieve(self, request, *args, **kwargs):
        if request.user is not None:
            # user_serializer = self.serializer_class(instance=request.user)
            user_serializer = UserAccountSerializer(instance=request.user)
            return ResponseWrapper(data=user_serializer.data, status=200)
        else:
            return ResponseWrapper(data={}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("name", openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ]
    )
    def search_user(self, request, *args, **kwargs):
        search_params = request.query_params.get("name")
        usr = UserAccount.objects.get_user_suggestions(search_params)
        serializer = UserAccountSerializer(instance=usr, many=True)
        return Response(data=serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user is not None:
            user_serializer = UserAccountSerializer(
                instance=request.user, data={}, partial=True
            )
            user_serializer.update(
                instance=request.user, validated_data={"status": "DEL"}
            )
            if user_serializer.is_valid():
                return ResponseWrapper(data=user_serializer.data, status=200)
        return ResponseWrapper(data="Active account not found", status=400)
