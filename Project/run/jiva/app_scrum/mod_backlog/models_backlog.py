from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

class Backlog(MPTTModel):
    """
    Represents a Scrum Backlog item using MPTT to create a hierarchical structure.
    This allows for epics, features, user stories, tasks, etc. to be organized in a tree.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Tree structure - allows for nesting of backlog items
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                            related_name='children')
    
    # Status and priority
    status = models.CharField(
        max_length=20,
        choices=[
            ('to_do', 'To Do'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('blocked', 'Blocked'),
        ],
        default='to_do'
    )
    
    priority = models.CharField(
        max_length=20,
        choices=[
            ('critical', 'Critical'),
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ],
        default='medium'
    )
    
    # Estimation and tracking
    story_points = models.IntegerField(null=True, blank=True)
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Relationships - commented out until the related models are implemented
    # sprint = models.ForeignKey('mod_sprint.Sprint', on_delete=models.SET_NULL, 
    #                           null=True, blank=True, related_name='backlog_items')
    # backlog_type = models.ForeignKey('mod_backlog_type.BacklogType', 
    #                                 on_delete=models.SET_NULL, null=True, blank=True)
    # assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, 
    #                               null=True, blank=True, related_name='assigned_backlog_items')
    
    # Standard fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, 
                                  null=True, related_name='created_backlog_items')
    active = models.BooleanField(default=True)
    
    class MPTTMeta:
        order_insertion_by = ['priority', 'created_at']
    
    class Meta:
        verbose_name = 'Backlog Item'
        verbose_name_plural = 'Backlog Items'
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Check if the backlog item is overdue"""
        if self.end_date and self.status != 'done':
            return self.end_date < timezone.now().date()
        return False
    
    def get_absolute_url(self):
        """Get the absolute URL for the backlog item"""
        return f"/app_scrum/backlog/{self.id}/"