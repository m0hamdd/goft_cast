from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from .managers import UserManager
from django.core.exceptions import ValidationError
import re

# Create your models here.

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15 , unique=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    display_name = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    total_donate = models.PositiveBigIntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'email', 'display_name']

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self) :
        return self.phone_number
    
    # def __str__(self) :
    #     return self.email

    def has_perm(self , perm , obj=None):
        return True
    
    def has_module_perms(self , app_label):
        return True
    
    def clean(self):
        if not re.match(r'^\d{10,15}$', self.phone_number):
            raise ValidationError("Phone number format is incorrect")

    @property
    def is_staff(self):
        return self.is_admin


class OtpCodeModel(models.Model):
    phone_number = models.CharField(max_length=11)
    otp          = models.PositiveSmallIntegerField()
    created      = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.phone_number} - {self.otp} - {self.created}'

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کد تایید"