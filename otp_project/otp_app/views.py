from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .managers import OTPManager

otp_manager = OTPManager()


@api_view(['POST'])
def request_otp(request):
    """Request OTP for phone verification"""
    phone = request.data.get('phone')

    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    otp_device = otp_manager.generate_otp(user)
    return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_otp(request):
    """Verify OTP entered by the user"""
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if otp_manager.verify_otp(user, otp):
        return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid OTP or OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
