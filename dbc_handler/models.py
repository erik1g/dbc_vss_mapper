from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
import uuid

class DBCData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='dbc_data')
    title = models.CharField(max_length=255)
    parsed_data = models.JSONField(default=dict) 
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project})"

