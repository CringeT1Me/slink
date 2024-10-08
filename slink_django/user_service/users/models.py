from cities_light.models import City, Country

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from users.managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = {
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    }
    username = models.CharField(_('username'), validators=[MinLengthValidator(6)],
                                max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=30,
                             null=True, blank=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=20)
    last_name = models.CharField(_('last name'), max_length=20)
    city = models.ForeignKey(City, on_delete=models.SET_NULL,
                             null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                null=True, blank=True)
    description = models.CharField(_('description'), max_length=100,
                                   null=True, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    last_online = models.DateTimeField(_('last online'), default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_of_birthday = models.DateField(_('date of birthday'), null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default=MALE)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password',]

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        unique_together = ('username', 'email', 'phone')

