# from django.contrib.auth import get_user_model

# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed

# from apps.accounts.services.jwt_service import JWTService

# User = get_user_model()
# import traceback

# class JWTAuthentication(BaseAuthentication):
#     """
#     Custom JWT Authentication using PyJWT.
#     """

#     def authenticate(self, request):

#         # ---------------------------------------
#         # Authorization Header
#         # ---------------------------------------

#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return None

#         parts = auth_header.split()

#         if len(parts) != 2:
#             raise AuthenticationFailed(
#                 "Invalid Authorization header."
#             )

#         if parts[0] != "Bearer":
#             raise AuthenticationFailed(
#                 "Authorization header must start with Bearer."
#             )

#         token = parts[1]

#         # ---------------------------------------
#         # Verify JWT
#         # ---------------------------------------
#         print("=" * 50)
#         print("Authorization Header:", auth_header)

#         parts = auth_header.split()

#         print("Parts:", parts)

#         token = parts[1]

#         print("Token:", repr(token))

#         print("STEP 1")
#         try:
#          payload = JWTService.verify_access_token(token)
#          print("Payload:", payload)
#         except Exception as e:
#         print("ERROR OCCURRED")
#         traceback.print_exc()
#         print(type(e))
#         print(e)
#         raise

#         print("STEP 2")
#         user_id = payload.get("user_id")
#         print("user_id:", user_id)
#         if not user_id:
#             raise AuthenticationFailed(
#                 "Invalid access token."
#             )

#         # ---------------------------------------
#         # Get User
#         # ---------------------------------------

#         try:

#             user = User.objects.get(
#                 id=user_id,
#                 is_active=True
#             )

#         except User.DoesNotExist:

#             raise AuthenticationFailed(
#                 "User not found."
#             )

#         return (
#             user,
#             token
#         )


from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.accounts.services.jwt_service import JWTService

import traceback
import inspect

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication using PyJWT.
    """

    def authenticate(self, request):

        # ---------------------------------------
        # Authorization Header
        # ---------------------------------------

        print("\n" + "=" * 80)
        print("JWT Authentication Started")
        print("=" * 80)

        auth_header = request.headers.get("Authorization")

        print("Authorization Header:", auth_header)

        if not auth_header:
            print("No Authorization Header Found")
            return None

        parts = auth_header.split()

        print("Header Parts:", parts)

        if len(parts) != 2:
            print("Invalid Header Length")
            raise AuthenticationFailed(
                "Invalid Authorization header."
            )

        if parts[0] != "Bearer":
            print("Bearer Keyword Missing")
            raise AuthenticationFailed(
                "Authorization header must start with Bearer."
            )

        token = parts[1]

        print("Token:", repr(token))
        print()

        # ---------------------------------------
        # JWTService Information
        # ---------------------------------------

        print("JWTService Class:", JWTService)
        print("JWTService File:", inspect.getfile(JWTService))
        print("Available Methods:", dir(JWTService))
        print()

        # ---------------------------------------
        # Verify JWT
        # ---------------------------------------

        print("STEP 1 : Before verify_access_token()")

        try:

            payload = JWTService.verify_access_token(token)

            print("STEP 2 : verify_access_token() Returned Successfully")
            print("Payload:", payload)

        except Exception as e:

            print("\n" + "=" * 80)
            print("ERROR INSIDE verify_access_token()")
            print("=" * 80)

            traceback.print_exc()

            print()
            print("Exception Type :", type(e))
            print("Exception :", str(e))

            raise

        print("STEP 3 : After verify_access_token()")

        user_id = payload.get("user_id")

        print("User ID:", user_id)

        if not user_id:
            raise AuthenticationFailed(
                "Invalid access token."
            )

        # ---------------------------------------
        # Get User
        # ---------------------------------------

        print("STEP 4 : Fetching User")

        try:

            user = User.objects.get(
                id=user_id,
                is_active=True
            )

            print("User Found:", user)

        except User.DoesNotExist:

            print("User Not Found")

            raise AuthenticationFailed(
                "User not found."
            )

        print("Authentication Successful")

        return (
            user,
            token
        )
    