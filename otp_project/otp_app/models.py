from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


# User model
class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '998900404001'. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # groups va user_permissions maydonlariga related_name qo'shish
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='otp_app_user_set',  # related_name ni o'zgartiring
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='otp_app_user_permissions_set',  # related_name ni o'zgartiring
        blank=True
    )
    #
    # def __str__(self):
    #     return self.username

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


# OTP TOTP uchun qurilma modeli (vaqtga asoslangan bir martalik parol)
# Custom OTPDevice model
class OTPDevice(TOTPDevice):
    custom_user = models.ForeignKey(get_user_model(),
                                    on_delete=models.CASCADE)  # 'user' o'rniga 'custom_user' nomini ishlatish
    otp = models.IntegerField()
    expiry_time = models.DateTimeField()

    def __str__(self):
        return f"{self.custom_user.phone} - {self.otp}"