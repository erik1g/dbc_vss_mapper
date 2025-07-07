from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
import uuid

User = get_user_model()

class VSSData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='vss_data')
    title = models.CharField(max_length=255)
    data = models.JSONField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project})"

class VSSSignal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vss_data = models.ForeignKey(
        VSSData,
        on_delete=models.CASCADE,
        related_name='vss_signals'
    )
    name = models.CharField(max_length=255)
    api_name = models.CharField(max_length=1024)
    type = models.CharField(max_length=64)   # branch / sensor / actuator / attribute
    datatype = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    api_id = models.CharField(max_length=128, blank=True, null=True)
    api_uuid = models.CharField(max_length=128, blank=True, null=True)
    parent_api_name = models.CharField(max_length=1024, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.vss_data.title})"



