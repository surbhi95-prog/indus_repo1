
# apps/accounts/services/auth_service.py

from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework.exceptions import AuthenticationFailed, ValidationError

from apps.accounts.models import User
from apps.accounts.models.user_session import UserSession

from apps.accounts.services.jwt_service import JWTService


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
    def login(email, password, request=None):
        """
        Authenticate user and create login session.
        """

        email = email.strip().lower()

        # -----------------------------------------------------
        # Find User
        # -----------------------------------------------------

        try:
            user = User.objects.select_related(
                "company",
                "plant",
                "department",
                "employee",
            ).get(
                email=email
            )

        except User.DoesNotExist:
            raise AuthenticationFailed(
                "Invalid email or password."
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
                "Invalid email or password."
            )

        # -----------------------------------------------------
        # Generate Tokens
        # -----------------------------------------------------

        access_token = JWTService.generate_access_token(
            user=user
        )

        refresh_token = JWTService.generate_refresh_token(
            user=user
        )

        # -----------------------------------------------------
        # Create Session
        # -----------------------------------------------------

        session = AuthService.create_session(
            user=user,
            refresh_token=refresh_token,
            request=request
        )

        # -----------------------------------------------------
        # Response
        # -----------------------------------------------------

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "session": session,
        }

    # =========================================================
    # CREATE SESSION
    # =========================================================

    @staticmethod
    def create_session(
        user,
        refresh_token,
        request=None
    ):
        """
        Create user login session.
        """

        ip_address = None
        user_agent = None

        if request:

            # -------------------------------------------------
            # IP Address
            # -------------------------------------------------

            x_forwarded_for = request.META.get(
                "HTTP_X_FORWARDED_FOR"
            )

            if x_forwarded_for:
                ip_address = (
                    x_forwarded_for.split(",")[0]
                    .strip()
                )

            else:
                ip_address = request.META.get(
                    "REMOTE_ADDR"
                )

            # -------------------------------------------------
            # User Agent
            # -------------------------------------------------

            user_agent = request.META.get(
                "HTTP_USER_AGENT"
            )

        # -----------------------------------------------------
        # Create Session
        # -----------------------------------------------------

        session = UserSession.objects.create(
            user=user,
            refresh_token=refresh_token,
            ip_address=ip_address,
            user_agent=user_agent,
            is_active=True,
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
        # Generate New Access Token
        # -----------------------------------------------------

        access_token = JWTService.generate_access_token(
            user=user
        )

        return {
            "user": user,
            "access_token": access_token,
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
            deactivate all sessions.
        """

        if refresh_token:

            updated = UserSession.objects.filter(
                user=user,
                refresh_token=refresh_token,
                is_active=True,
            ).update(
                is_active=False
            )

        else:

            updated = UserSession.objects.filter(
                user=user,
                is_active=True,
            ).update(
                is_active=False
            )

        return updated

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

        if not user.is_active:

            raise AuthenticationFailed(
                "User account is inactive."
            )

        return user

