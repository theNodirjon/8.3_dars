import random
from django.utils import timezone
from datetime import timedelta
from twilio.rest import Client  # Twilio client
from django.conf import settings  # Sozlamalardan foydalanish
from .models import OTPDevice

class OTPManager:
    def generate_otp(self, user):
        """Generate a 6-digit OTP"""
        otp = random.randint(100000, 999999)
        otp_expiry_time = timezone.now() + timedelta(minutes=3)

        # Otp va yaroqlilik muddatini vaqtinchalik jadvalda yoki foydalanuvchi modelidagi maydon sifatida saqlash
        otp_device = OTPDevice.objects.create(user=user, otp=otp, expiry_time=otp_expiry_time)

        # Twilio API orqali SMS yuborish
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your OTP code is {otp}. It will expire in 3 minutes.',
                from_=settings.TWILIO_PHONE_NUMBER,  # Twilio raqami
                to=user.phone  # Foydalanuvchining telefon raqami
            )
        except Exception as e:
            print(f"Error sending OTP: {e}")
            return None  # Agar SMS yuborishda xatolik bo'lsa, None qaytaradi

        return otp_device

    def verify_otp(self, user, otp):
        """Foydalanuvchi tomonidan kiritilgan OTP-ni tasdiqlash"""
        try:
            otp_device = OTPDevice.objects.get(user=user, otp=otp)
            if otp_device.expiry_time < timezone.now():
                return False  # OTP has expired
            return True
        except OTPDevice.DoesNotExist:
            return False
