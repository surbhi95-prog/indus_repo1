
# apps/accounts/services/auth_service.py

# from django.db import transaction
# from django.contrib.auth import authenticate

# from rest_framework.exceptions import AuthenticationFailed, ValidationError

# from apps.accounts.models import User
# from apps.accounts.models.user_session import UserSession

# from apps.accounts.services.jwt_service import JWTService


# class AuthService:
#     """
#     Authentication Service

#     Responsibilities:
#         - Login
#         - Generate JWT tokens
#         - Create user session
#         - Refresh token
#         - Logout
#         - Get current user
#     """

#     # =========================================================
#     # LOGIN
#     # =========================================================

#     @staticmethod
#     @transaction.atomic
#     def login(email, password, request=None):
#         """
#         Authenticate user and create login session.
#         """

#         email = email.strip().lower()

#         # -----------------------------------------------------
#         # Find User
#         # -----------------------------------------------------

#         try:
#             user = User.objects.select_related(
#                 "company",
#                 "plant",
#                 "department",
#                 "employee",
#             ).get(
#                 email=email
#             )

#         except User.DoesNotExist:
#             raise AuthenticationFailed(
#                 "Invalid email or password."
#             )

#         # -----------------------------------------------------
#         # Check Active
#         # -----------------------------------------------------

#         if not user.is_active:
#             raise AuthenticationFailed(
#                 "User account is inactive."
#             )

#         # -----------------------------------------------------
#         # Check Password
#         # -----------------------------------------------------

#         if not user.check_password(password):
#             raise AuthenticationFailed(
#                 "Invalid email or password."
#             )

#         # -----------------------------------------------------
#         # Generate Tokens
#         # -----------------------------------------------------

#         access_token = JWTService.generate_access_token(
#             user=user
#         )

#         refresh_token = JWTService.generate_refresh_token(
#             user=user
#         )

#         # -----------------------------------------------------
#         # Create Session
#         # -----------------------------------------------------

#         session = AuthService.create_session(
#             user=user,
#             refresh_token=refresh_token,
#             request=request
#         )

#         # -----------------------------------------------------
#         # Response
#         # -----------------------------------------------------

#         return {
#             "user": user,
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "session": session,
#         }

#     # =========================================================
#     # CREATE SESSION
#     # =========================================================

#     @staticmethod
#     def create_session(
#         user,
#         refresh_token,
#         request=None
#     ):
#         """
#         Create user login session.
#         """

#         ip_address = None
#         user_agent = None

#         if request:

#             # -------------------------------------------------
#             # IP Address
#             # -------------------------------------------------

#             x_forwarded_for = request.META.get(
#                 "HTTP_X_FORWARDED_FOR"
#             )

#             if x_forwarded_for:
#                 ip_address = (
#                     x_forwarded_for.split(",")[0]
#                     .strip()
#                 )

#             else:
#                 ip_address = request.META.get(
#                     "REMOTE_ADDR"
#                 )

#             # -------------------------------------------------
#             # User Agent
#             # -------------------------------------------------

#             user_agent = request.META.get(
#                 "HTTP_USER_AGENT"
#             )

#         # -----------------------------------------------------
#         # Create Session
#         # -----------------------------------------------------

#         session = UserSession.objects.create(
#             user=user,
#             refresh_token=refresh_token,
#             ip_address=ip_address,
#             user_agent=user_agent,
#             is_active=True,
#         )

#         return session

#     # =========================================================
#     # REFRESH TOKEN
#     # =========================================================

#     @staticmethod
#     @transaction.atomic
#     def refresh_token(refresh_token):
#         """
#         Validate refresh token and generate
#         a new access token.
#         """

#         # -----------------------------------------------------
#         # Verify Refresh Token
#         # -----------------------------------------------------

#         payload = JWTService.verify_refresh_token(
#             refresh_token
#         )

#         user_id = payload.get("user_id")

#         if not user_id:
#             raise AuthenticationFailed(
#                 "Invalid refresh token."
#             )

#         # -----------------------------------------------------
#         # Get User
#         # -----------------------------------------------------

#         try:

#             user = User.objects.select_related(
#                 "company",
#                 "plant",
#                 "department",
#                 "employee",
#             ).get(
#                 id=user_id
#             )

#         except User.DoesNotExist:

#             raise AuthenticationFailed(
#                 "User not found."
#             )

#         # -----------------------------------------------------
#         # Check User
#         # -----------------------------------------------------

#         if not user.is_active:

#             raise AuthenticationFailed(
#                 "User account is inactive."
#             )

#         # -----------------------------------------------------
#         # Check Session
#         # -----------------------------------------------------

#         session = UserSession.objects.filter(
#             user=user,
#             refresh_token=refresh_token,
#             is_active=True,
#         ).first()

#         if not session:

#             raise AuthenticationFailed(
#                 "Session expired or logged out."
#             )

#         # -----------------------------------------------------
#         # Generate New Access Token
#         # -----------------------------------------------------

#         access_token = JWTService.generate_access_token(
#             user=user
#         )

#         return {
#             "user": user,
#             "access_token": access_token,
#         }

#     # =========================================================
#     # LOGOUT
#     # =========================================================

#     @staticmethod
#     @transaction.atomic
#     def logout(user, refresh_token=None):
#         """
#         Logout user.

#         If refresh_token is supplied:
#             deactivate only that session.

#         Otherwise:
#             deactivate all sessions.
#         """

#         if refresh_token:

#             updated = UserSession.objects.filter(
#                 user=user,
#                 refresh_token=refresh_token,
#                 is_active=True,
#             ).update(
#                 is_active=False
#             )

#         else:

#             updated = UserSession.objects.filter(
#                 user=user,
#                 is_active=True,
#             ).update(
#                 is_active=False
#             )

#         return updated

#     # =========================================================
#     # GET CURRENT USER
#     # =========================================================

#     @staticmethod
#     def get_current_user(user_id):
#         """
#         Get currently authenticated user.
#         """

#         try:

#             user = User.objects.select_related(
#                 "company",
#                 "plant",
#                 "department",
#                 "employee",
#             ).get(
#                 id=user_id
#             )

#         except User.DoesNotExist:

#             raise AuthenticationFailed(
#                 "User not found."
#             )

#         if not user.is_active:

#             raise AuthenticationFailed(
#                 "User account is inactive."
#             )

#         return user


from datetime import datetime, timezone as dt_timezone

from django.db import transaction, models
from django.utils import timezone

from rest_framework.exceptions import (
    AuthenticationFailed,
    ValidationError,
)

from apps.accounts.models import User
from apps.accounts.models.user_session import UserSession
from apps.accounts.services.jwt_service import JWTService
from apps.accounts.models.user_role import UserRole
from apps.accounts.models.role_permission import RolePermission


class AuthService:
    """
    Authentication Service

    Responsibilities:
        - Login
        - Generate JWT tokens
        - Create user session
        - Refresh token
        - Logout
        - Get current user
    """

    # =========================================================
    # LOGIN
    # =========================================================

    
    @staticmethod
    @transaction.atomic
    def login(login, password, request=None):
        """
        Authenticate user using either email or username
        and create login session.
        """

        login = login.strip().lower()

        # -----------------------------------------------------
        # Find User By Email OR Employee Username
        # -----------------------------------------------------

        user = (
            User.objects
            .select_related(
                "company",
                "plant",
                "department",
                "employee",
            )
            .filter(
                models.Q(email__iexact=login)
                | models.Q(employee__username__iexact=login)
            )
            .first()
        )

        if not user:
            raise AuthenticationFailed(
                "Invalid email/username or password."
            )

        # -----------------------------------------------------
        # Check Active
        # -----------------------------------------------------

        if not user.is_active:
            raise AuthenticationFailed(
                "User account is inactive."
            )

        # -----------------------------------------------------
        # Check Password
        # -----------------------------------------------------

        if not user.check_password(password):
            raise AuthenticationFailed(
                "Invalid email/username or password."
            )

        # # -----------------------------------------------------
        # # Check Active
        # # -----------------------------------------------------

        # if not user.is_active:
        #     raise AuthenticationFailed(
        #         "User account is inactive."
        #     )

        # # -----------------------------------------------------
        # # Check Password
        # # -----------------------------------------------------

        # if not user.check_password(password):
        #     raise AuthenticationFailed(
        #         "Invalid email or password."
        #     )

        # -----------------------------------------------------
        # Generate Access Token
        # -----------------------------------------------------

        access_token = JWTService.generate_access_token(
            user=user
        )

        # -----------------------------------------------------
        # Generate Refresh Token
        # -----------------------------------------------------

        refresh_token = JWTService.generate_refresh_token(
            user=user
        )

        # -----------------------------------------------------
        # Create Session
        # -----------------------------------------------------

        session = AuthService.create_session(
            user=user,
            refresh_token=refresh_token,
            request=request,
        )
                # -----------------------------------------------------
        # Get User Roles & Permissions
        # -----------------------------------------------------

        user_roles = UserRole.objects.filter(
            user=user
        ).select_related(
            "role"
        )

        roles_data = []

        for user_role in user_roles:

            role = user_role.role

            # -------------------------------------------------
            # Skip invalid role assignment
            # -------------------------------------------------

            if not role:
                continue

            # -------------------------------------------------
            # Get Role Permissions
            # -------------------------------------------------

            role_permissions = RolePermission.objects.filter(
                role=role
            ).select_related(
                "permission"
            )

            permissions = []

            for role_permission in role_permissions:

                # ---------------------------------------------
                # Skip invalid permission
                # ---------------------------------------------

                if not role_permission.permission:
                    continue

                permission_code = (
                    role_permission.permission.code
                )

                if permission_code not in permissions:
                    permissions.append(permission_code)

            # -------------------------------------------------
            # Add Role
            # -------------------------------------------------

            roles_data.append({
                "roleKey": role.code,
                "name": role.name,
                "scope": (
                    role.scope.strip().lower()
                    if role.scope
                    else None
                ),
                "permissions": permissions,
            })

        # -----------------------------------------------------
        # Response
        # -----------------------------------------------------

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
           
            "session_id": str(session.id),
            "roles": roles_data,
        }

    # =========================================================
    # CREATE SESSION
    # =========================================================

    @staticmethod
    def create_session(
        user,
        refresh_token,
        request=None,
    ):
        """
        Create user login session.
        """

        # -----------------------------------------------------
        # Default Values
        # -----------------------------------------------------

        ip_address = "127.0.0.1"
        user_agent = ""
        device_type = "unknown"
        device_name = "unknown"

        # -----------------------------------------------------
        # Request Information
        # -----------------------------------------------------

        if request:

            # -------------------------------------------------
            # IP Address
            # -------------------------------------------------

            x_forwarded_for = request.META.get(
                "HTTP_X_FORWARDED_FOR"
            )

            if x_forwarded_for:

                ip_address = (
                    x_forwarded_for
                    .split(",")[0]
                    .strip()
                )

            else:

                ip_address = request.META.get(
                    "REMOTE_ADDR",
                    "127.0.0.1",
                )

            # -------------------------------------------------
            # User Agent
            # -------------------------------------------------

            user_agent = request.META.get(
                "HTTP_USER_AGENT",
                "",
            )

            # -------------------------------------------------
            # Device Detection
            # -------------------------------------------------

            if "PostmanRuntime" in user_agent:

                device_type = "api"
                device_name = "Postman"

            elif "Mobile" in user_agent:

                device_type = "mobile"
                device_name = "Mobile Browser"

            elif "Mozilla" in user_agent:

                device_type = "browser"
                device_name = "Web Browser"

            else:

                device_type = "unknown"
                device_name = "unknown"

        # -----------------------------------------------------
        # Verify Refresh Token
        # -----------------------------------------------------

        # payload = JWTService.verify_refresh_token(
        #     refresh_token
        # )
        try:
            payload = JWTService.verify_refresh_token(
                refresh_token
            )
        except AuthenticationFailed:
            raise AuthenticationFailed(
                "Login failed while creating session."
            )
                # -----------------------------------------------------
        # Get Refresh Token Expiration
        # -----------------------------------------------------

        expires_at = datetime.fromtimestamp(
            payload["exp"],
            tz=dt_timezone.utc,
        )

        # -----------------------------------------------------
        # Create Session
        # -----------------------------------------------------

        session = UserSession.objects.create(
            user=user,

            refresh_token=refresh_token,

            device_type=device_type,
            device_name=device_name,

            user_agent=user_agent,

            ip_address=ip_address,

            is_active=True,

            expires_at=expires_at,

            last_activity=timezone.now(),
        )

        return session

    # =========================================================
    # REFRESH TOKEN
    # =========================================================

    @staticmethod
    @transaction.atomic
    def refresh_token(refresh_token):
        """
        Validate refresh token and generate
        a new access token.
        """

        # -----------------------------------------------------
        # Verify Refresh Token
        # -----------------------------------------------------

        payload = JWTService.verify_refresh_token(
            refresh_token
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticationFailed(
                "Invalid refresh token."
            )

        # -----------------------------------------------------
        # Get User
        # -----------------------------------------------------

        try:

            user = User.objects.select_related(
                "company",
                "plant",
                "department",
                "employee",
            ).get(
                id=user_id
            )

        except User.DoesNotExist:

            raise AuthenticationFailed(
                "User not found."
            )

        # -----------------------------------------------------
        # Check User
        # -----------------------------------------------------

        if not user.is_active:

            raise AuthenticationFailed(
                "User account is inactive."
            )

        # -----------------------------------------------------
        # Check Session
        # -----------------------------------------------------

        session = UserSession.objects.filter(
            user=user,
            refresh_token=refresh_token,
            is_active=True,
        ).first()

        if not session:

            raise AuthenticationFailed(
                "Session expired or logged out."
            )

        # -----------------------------------------------------
        # Check Session Expiration
        # -----------------------------------------------------

        if session.expires_at <= timezone.now():

            session.is_active = False

            session.logged_out_at = timezone.now()

            session.save(
                update_fields=[
                    "is_active",
                    "logged_out_at",
                ]
            )

            raise AuthenticationFailed(
                "Session has expired."
            )

        # -----------------------------------------------------
        # Update Last Activity
        # -----------------------------------------------------

        session.last_activity = timezone.now()

        session.save(
            update_fields=[
                "last_activity"
            ]
        )

        # -----------------------------------------------------
        # Generate New Access Token
        # -----------------------------------------------------

        access_token = JWTService.generate_access_token(
            user=user
        )

        new_refresh_token = JWTService.generate_refresh_token(
            user=user
            )

# -----------------------------------------------------
# Update Session With New Refresh Token
# -----------------------------------------------------

        session.refresh_token = new_refresh_token
        session.last_activity = timezone.now()

        session.save(
    update_fields=[
        "refresh_token",
        "last_activity",
    ]
)

        return {
    "access_token": access_token,
    "refresh_token": new_refresh_token,
    "user": {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
}

    # =========================================================
    # LOGOUT
    # =========================================================

    @staticmethod
    @transaction.atomic
    def logout(user, refresh_token=None):
        """
        Logout user.

        If refresh_token is supplied:
            deactivate only that session.

        Otherwise:
            deactivate all active sessions.
        """

        if refresh_token:

            updated = UserSession.objects.filter(
                user=user,
                refresh_token=refresh_token,
                is_active=True,
            ).update(
                is_active=False,
                logged_out_at=timezone.now(),
            )

            if updated == 0:
                return {
                    "success": False,
                    "message": "Session not found or already logged out.",
                }

            return {
                "success": True,
                "message": "Logout successful.",
            }

        updated = UserSession.objects.filter(
            user=user,
            is_active=True,
        ).update(
            is_active=False,
            logged_out_at=timezone.now(),
        )

        return {
            "success": True,
            "message": f"{updated} active session(s) logged out.",
        }

    # =========================================================
    # GET CURRENT USER
    # =========================================================

    @staticmethod
    def get_current_user(user_id):
        """
        Get currently authenticated user.
        """

        try:

            user = User.objects.select_related(
                "company",
                "plant",
                "department",
                "employee",
            ).get(
                id=user_id
            )

        except User.DoesNotExist:

            raise AuthenticationFailed(
                "User not found."
            )

        # -----------------------------------------------------
        # Check Active
        # -----------------------------------------------------

        if not user.is_active:

            raise AuthenticationFailed(
                "User account is inactive."
            )

        return user

