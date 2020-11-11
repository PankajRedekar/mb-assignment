from datetime import date

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api.managers import UserManager


class ManagerUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    Username field: Email
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    plans = models.ManyToManyField(to='Plan', through="Subscription")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Plan(models.Model):
    """
    Subscription Plans
    Monthly plans(validity=30)
    """
    title = models.CharField(max_length=200, unique=True)
    validity = models.IntegerField(default=30)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)


class Subscription(models.Model):
    """
    Suscriptions.
    User should have Plan by subscription.
    """
    user = models.ForeignKey(ManagerUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)


class CreditCard(models.Model):
    """
    Credit card 
    Each user only one credit card
    """
    user = models.OneToOneField(ManagerUser, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200)
    credit_card_number_validator = RegexValidator(r"(?:[0-9]{4}){3}[0-9]{4}|[0-9]{16}")
    number = models.CharField(max_length=16, validators=[credit_card_number_validator])
    name_on_card = models.CharField(max_length=200)
    expiry_date = models.DateField()
    cvv_validator = RegexValidator(r"^[0-9]{3}$")
    cvv = models.CharField(max_length=3, validators=[cvv_validator,])

    def save(self, *args, **kwargs):
        if self.expiry_date < date.today():
            raise ValidationError("The date cannot be in the past!")

        super(CreditCard, self).save(*args, **kwargs)