from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid


class pcinfo(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        null=False,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False
    )
    name = models.CharField(
        max_length=140,
        null=False,
    )
    description = models.TextField(
        null=True
    )
    timestamp = models.DateTimeField(
        auto_now=True,
        null=False
    )

class pcdata(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        null=False,
    )
    pc = models.ForeignKey(
        pcinfo,
        on_delete=models.CASCADE,
        null=False
    )
    cpu_json = models.JSONField(
        blank=True,
        null=True
    )
    gpu_json = models.JSONField(
        blank=True,
        null=True
    )
    memory_json = models.JSONField(
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        auto_now=True,
        null=False,
    )