from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
import uuid

class VssDbcMappingData (models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='vss_dbc_mapping')
    title = models.CharField(max_length=255, blank=True, null=True)
    mapping_data = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Mapping between VSS and DBC data"
    
    class Meta:
        verbose_name = "VSS-DBC Mapping Data"
        verbose_name_plural = "VSS-DBC Mapping Data"
