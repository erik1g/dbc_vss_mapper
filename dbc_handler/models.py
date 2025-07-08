from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
import uuid

class DBCData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='dbc_data')
    title = models.CharField(max_length=255)
    data = models.JSONField(default=dict) 
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project})"
    
class DBCMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dbc_data = models.ForeignKey(DBCData, on_delete=models.CASCADE, related_name='messages')
    
    name = models.CharField(max_length=255)
    frame_id = models.CharField(max_length=64, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    senders = models.JSONField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class DBCSignal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(DBCMessage, on_delete=models.CASCADE, related_name='signals')

    # --- Signal-spezifisch ---
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=64, blank=True, null=True)
    start_bit = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    byte_order = models.CharField(max_length=32, blank=True, null=True)
    is_signed = models.BooleanField(default=False)
    scale = models.FloatField(blank=True, null=True)
    offset = models.FloatField(blank=True, null=True)
    minimum = models.FloatField(blank=True, null=True)
    maximum = models.FloatField(blank=True, null=True)
    choices = models.JSONField(blank=True, null=True)

    # --- Optional für zusätzliche Dinge
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.message.name})"