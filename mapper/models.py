from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
import uuid

class VssDbcMappingData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='vss_dbc_mappings')
    title = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mapping for Project: {self.project.title}"

    class Meta:
        verbose_name = "VSS-DBC Mapping Data"
        verbose_name_plural = "VSS-DBC Mapping Data"


class VssDbcMappingEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mapping_data = models.ForeignKey(VssDbcMappingData,on_delete=models.CASCADE,related_name='entries')
    vss_signal = models.ForeignKey('vss_handler.VSSSignal',on_delete=models.CASCADE,related_name='mappings')
    dbc_signal = models.ForeignKey('dbc_handler.DBCSignal',on_delete=models.CASCADE,related_name='mappings')
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.mapping_data.project.title}: {self.vss_signal} ↔ {self.dbc_signal}"
    
    class Meta:
        unique_together = ('mapping_data', 'vss_signal')

class VssDbcMappingTransform(models.Model):
    DIRECTION_CHOICES = [
        ('dbc2vss', 'DBC to VSS'),
        ('vss2dbc', 'VSS to DBC')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mapping_entry = models.ForeignKey(VssDbcMappingEntry,on_delete=models.CASCADE,related_name='transforms')
    direction = models.CharField(max_length=16, choices=DIRECTION_CHOICES)
    interval_ms = models.IntegerField(blank=True, null=True)
    math = models.CharField(max_length=255, blank=True, null=True)
    mapping = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mapping_entry} [{self.direction}]"
