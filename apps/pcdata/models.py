from django.db import models

from django.conf import settings
# from django.contrib.auth.models import User
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
        on_delete=models.DO_NOTHING,
        null=False,
    )
    name = models.CharField(
        max_length=140,
        null=False,
    )
    other_info = models.TextField(
        null=True,
    )
    os = models.TextField(
        max_length=140,
        null=True,
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
    )
    date_added = models.DateTimeField(
        auto_now=True, #TODO When updating, can't change this data
        null=False,
    )

class pcdata(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        null=False,
    )
    pc = models.ForeignKey(
        pcinfo,
        on_delete=models.DO_NOTHING,
        null=False,
    )
    cpu_json = models.JSONField(
        blank=True,
        null=True
    )
    gpu_json = models.JSONField(
        blank=True,
        null=True,
    )
    memory_json = models.JSONField(
        blank=True,
        null=True,
    )
    timestamp = models.DateTimeField(
        auto_now=True,
        null=False,
    )