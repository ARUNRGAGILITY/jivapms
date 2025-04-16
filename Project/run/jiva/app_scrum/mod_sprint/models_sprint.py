from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel

class Sprint(models.Model):
    """
    Represents a Scrum Sprint
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    goal = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('planning', 'Planning'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='planning'
    )
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    
    # Relationships
    # These will be implemented when the related models are created
    # product = models.ForeignKey('mod_product.Product', on_delete=models.CASCADE, null=True, blank=True)
    # project = models.ForeignKey('mod_project.Project', on_delete=models.CASCADE, null=True, blank=True)
    
    # Standard fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, 
                                  related_name='created_sprints')
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
    
    def __str__(self):
        return self.name
    
    def is_active(self):
        """Check if the sprint is currently active"""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.status == 'in_progress'
    
    def get_duration_days(self):
        """Calculate the duration of the sprint in days"""
        return (self.end_date - self.start_date).days