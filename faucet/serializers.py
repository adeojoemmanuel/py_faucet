from rest_framework import serializers

class WalletAddressSerializer(serializers.Serializer):
    wallet_address = serializers.CharField(max_length=42)