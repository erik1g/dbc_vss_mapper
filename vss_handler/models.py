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
    signals = models.JSONField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project})"


