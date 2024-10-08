from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import User
import requests

