# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.accounts.serializers.logout_serializer import LogoutSerializer
# from apps.accounts.services.auth_service import AuthService


# class LogoutView(APIView):
#     """
#     Logout API
#     """

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def post(self, request):

#         serializer = LogoutSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         response = AuthService.logout(
#             user=request.user,
#             refresh_token=serializer.validated_data["refresh_token"],
#             request=request
#         )

#         return Response(
#             response,
#             status=status.HTTP_200_OK
#         )


from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.logout_serializer import LogoutSerializer
from apps.accounts.services.auth_service import AuthService


class LogoutView(APIView):
    """
    Logout API
    """

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        response = AuthService.logout(
            user=request.user,
            refresh_token=serializer.validated_data["refresh_token"]
        )

        return Response(
            response,
            status=status.HTTP_200_OK
        )