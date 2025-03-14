
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Roadmapitem(BaseModelTrackImpl):
    STATUS_CHOICES = [
        ('done', 'Completed'),
        ('active', 'In Progress'),
        ('crit', 'Critical'),
        ('', ''),
    ]
    
    org = models.ForeignKey('Organization', on_delete=models.CASCADE, 
                            related_name='roadmap_items')
    section = models.CharField(max_length=255)  # e.g., "Year 1 - Foundations"
    task_name = models.CharField(max_length=255)  # e.g., "Define strategy"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_roadmap_items")

    def __str__(self):
        return f"{self.task_name} ({self.section})"