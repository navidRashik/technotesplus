from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status, viewsets, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from .serializers import TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer, TokenVerifyResponseSerializer, UserAccountPatchSerializer, UserAccountSerializer, UserSignupSerializer
from utils.response_wrapper import ResponseWrapper
from django.contrib.auth.hashers import make_password
from account_management.models import UserAccount
import uuid


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer})
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
        if self.action == "create" or self.action == "get_otp":
            permission_classes = [permissions.AllowAny]
        elif self.action in ["retrieve", "update"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            # permissions.DjangoObjectPermissions.has_permission()
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = UserAccount.objects.exclude(status="DEL")

    def create(self, request, *args, **kwargs):
        try:
            # email = request.data.pop("email", None)
            password = request.data.pop("password")
            username = request.data.get("username")
            verification_id = uuid.uuid4().__str__()
        except Exception as e:
            return ResponseWrapper(data=e.args, status=401)

        try:
            # temp_user = User.objects.
            # email_exist = User.objects.filter(email=email).exists()
            username_exist = UserAccount.objects.filter(
                username=username).exists()

            if username_exist:
                return ResponseWrapper(
                    data="Please use different username, it’s already been in use", status=400
                )
            password = make_password(password=password)
            user = UserAccount.objects.create(
                # email=email,
                password=password,
                # verification_id=verification_id,
                **request.data
            )
            # if user is None:
            #     return ResponseWrapper(data="Account already exist with given Email or Phone", status=401)
        except Exception as err:
            # logger.exception(msg="error while account cration")
            return ResponseWrapper(
                data="Account creation failed", status=401
            )

        # send_registration_confirmation_email(email)
        user_serializer = UserAccountSerializer(instance=user, many=False)
        return ResponseWrapper(data=user_serializer.data, status=200)

    def update(self, request, *args, **kwargs):
        password = request.data.pop("password", None)
        user_qs = UserAccount.objects.filter(pk=request.user.pk)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # if user_qs:
        if password:
            password = make_password(password=password)
            updated = user_qs.update(password=password, **request.data)
        else:
            updated = user_qs.update(**request.data)
        if not updated:
            return ResponseWrapper(error_code=status.HTTP_400_BAD_REQUEST, error_msg=['failed to update'])
        # is_apps = request.path.__contains__('/apps/')

        user_serializer = UserAccountSerializer(
            instance=user_qs.first(), many=False)
        return ResponseWrapper(data=user_serializer.data, status=200)

    def retrieve(self, request, *args, **kwargs):
        if request.user is not None:
            # user_serializer = self.serializer_class(instance=request.user)
            user_serializer = UserAccountSerializer(instance=request.user)
            return ResponseWrapper(data=user_serializer.data, status=200)
        else:
            return ResponseWrapper(data={}, status=status.HTTP_204_NO_CONTENT)

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

    # def get_otp(self, request, phone, *args, **kwargs):
    #     otp = random.randint(1000, 9999)
    #     otp_qs, _ = OtpUser.objects.get_or_create(phone=str(phone))
    #     if request.user.pk:
    #         otp_qs.user = request.user
    #     otp_qs.otp_code = otp
    #     otp_qs.save()

    #     if send_sms(body=f'Your OTP code for I-HOST is {otp} . Thanks for using I-HOST.', phone=str(phone)):
    #         return ResponseWrapper(msg='otp sent', data={'name': None, 'id': None, 'phone': phone}, status=200)
    #     else:
    #         return ResponseWrapper(error_msg='otp sending failed')
