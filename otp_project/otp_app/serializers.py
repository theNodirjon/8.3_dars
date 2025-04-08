from rest_framework import serializers

class OTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    otp = serializers.CharField(max_length=6)
