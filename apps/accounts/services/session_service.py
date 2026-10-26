


import hashlib

from django.conf import settings
from django.utils import timezone

from apps.accounts.models.user_session import UserSession


class SessionService:

    @staticmethod
    def hash_refresh_token(refresh_token):
        """
        Generate SHA256 hash of refresh token.
        """
        return hashlib.sha256(
            refresh_token.encode()
        ).hexdigest()

    @staticmethod
    def create_user_session(user, refresh_token, request):
        """
        Create or update a user session.

        If the user logs in again from the same device,
        update the existing session instead of creating a new one.
        """

        refresh_token_hash = SessionService.hash_refresh_token(
            refresh_token
        )

        device_name = request.META.get(
            "HTTP_USER_AGENT",
            "Unknown Device"
        )

        user_agent = request.META.get(
            "HTTP_USER_AGENT",
            ""
        )

        ip_address = request.META.get(
            "REMOTE_ADDR",
            "0.0.0.0"
        )

        session = UserSession.objects.filter(
            user=user,
            device_name=device_name,
            device_type="Web",
        ).first()

        if session:

            session.refresh_token_hash = refresh_token_hash
            session.user_agent = user_agent
            session.ip_address = ip_address
            session.last_activity = timezone.now()
            session.logged_out_at = None
            session.expires_at = (
                timezone.now() +
                settings.JWT_REFRESH_TOKEN_LIFETIME
            )
            session.is_active = True

            session.save(
                update_fields=[
                    "refresh_token_hash",
                    "user_agent",
                    "ip_address",
                    "last_activity",
                    "logged_out_at",
                    "expires_at",
                    "is_active",
                ]
            )

            return session

        return UserSession.objects.create(
            user=user,
            refresh_token_hash=refresh_token_hash,
            device_type="Web",
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=(
                timezone.now() +
                settings.JWT_REFRESH_TOKEN_LIFETIME
            ),
            last_activity=timezone.now(),
            is_active=True,
        )

    @staticmethod
    def update_last_activity(session):
        """
        Update last activity timestamp.
        """
        session.last_activity = timezone.now()
        session.save(
            update_fields=["last_activity"]
        )

    @staticmethod
    def logout(refresh_token):
        """
        Logout user session.
        """

        refresh_token_hash = SessionService.hash_refresh_token(
            refresh_token
        )

        session = UserSession.objects.filter(
            refresh_token_hash=refresh_token_hash,
            is_active=True
        ).first()

        if not session:
            return

        session.is_active = False
        session.logged_out_at = timezone.now()

        session.save(
            update_fields=[
                "is_active",
                "logged_out_at",
            ]
        )

    @staticmethod
    def logout_all_sessions(user):
        """
        Logout all active sessions of a user.
        """

        UserSession.objects.filter(
            user=user,
            is_active=True
        ).update(
            is_active=False,
            logged_out_at=timezone.now()
        )