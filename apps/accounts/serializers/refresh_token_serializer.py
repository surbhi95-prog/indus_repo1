from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    """
     Refresh Token Request Serializer 
     blank no clues of exact wi=orking of inventory management module
    """ 

    refresh_token = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        help_text="JWT Refresh Token"
    )