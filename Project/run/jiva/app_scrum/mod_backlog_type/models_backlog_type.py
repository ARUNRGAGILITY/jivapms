from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class BacklogType(MPTTModel):
    """
    Represents types of backlog items in a hierarchical structure.
    Examples: Epic, Feature, User Story, Task, Bug, etc.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Tree structure - enables a hierarchy of backlog types
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                            related_name='children')
    
    # Visual attributes
    icon = models.CharField(max_length=50, blank=True, null=True, 
                           help_text="CSS class for icon (e.g., 'bi bi-bug' for Bootstrap bug icon)")
    color = models.CharField(max_length=20, blank=True, null=True,
                            help_text="Color code (e.g., '#FF0000' for red)")
    
    # Defines which backlog types can be children of this type
    allowed_child_types = models.ManyToManyField('self', blank=True, symmetrical=False,
                                              related_name='allowed_as_child_of')
    
    # Standard fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, 
                                  null=True, related_name='created_backlog_types')
    active = models.BooleanField(default=True)
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = 'Backlog Type'
        verbose_name_plural = 'Backlog Types'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Get the absolute URL for the backlog type"""
        return f"/app_scrum/backlog_type/{self.id}/"
    
    def get_full_name(self):
        """Get the full hierarchical name (e.g., 'Epic > Feature > Story')"""
        ancestors = self.get_ancestors(include_self=True)
        return " > ".join(ancestor.name for ancestor in ancestors)