from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    """
    Logout Request Serializer
    """

    refresh_token = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )