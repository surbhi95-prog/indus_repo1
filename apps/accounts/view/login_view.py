# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView


# from apps.accounts.serializers.login_serializer import LoginSerializer
# from apps.accounts.services.auth_service import AuthService


# class LoginView(APIView):
#     """
#     Login Service
#     """
#     authentication_classes = []

#     permission_classes = []

#     def post(self,request):
#         """
#         Authenticate user and return jwt tokens
#         """

#         #. Validate Request Data

#         serializer = LoginSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )


#         # Authenticate User
        
#         result = AuthService.login(
#             email=serializer.validated_data["email"],
#             password=serializer.validated_data["password"],
#             request=request
#         )

#         return Response(
#             result,
#             status=status.HTTP_200_OK
#         )


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.accounts.serializers.login_serializer import (
    LoginSerializer,
    LoginUserSerializer,
)

from apps.accounts.services.auth_service import AuthService


class LoginView(APIView):
    """
    User Login API
    """

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        # -------------------------------------------------
        # Validate Request
        # -------------------------------------------------

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # -------------------------------------------------
        # Login
        # -------------------------------------------------

        result = AuthService.login(
            login=serializer.validated_data["login"],
            password=serializer.validated_data["password"],
            request=request,
        )

        # -------------------------------------------------
        # Serialize User
        # -------------------------------------------------

        user_data = LoginUserSerializer(
            result["user"]
        ).data

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": {
                    "user": user_data,

                    "access_token": result[
                        "access_token"
                    ],

                    "refresh_token": result[
                        "refresh_token"
                    ],
                    "session_id": result["session_id"],
                    "roles": result[
                "roles"
            ],
                }
            },
            status=status.HTTP_200_OK
        )