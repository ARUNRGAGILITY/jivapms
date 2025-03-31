from django.db import models
from django.utils import timezone
from app.app_postnote.mod_project.models_project import Project
# class Project(models.Model):
#     """Model for storing projects"""
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name

class PostNoteType(models.Model):
    """Model for storing post note types"""
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class PostNote(models.Model):
    """Simplified model for storing post notes"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='postnotes')
    title = models.CharField(max_length=255, default="New Item")
    description = models.TextField(blank=True, null=True, default="Click to edit description")
    type_name = models.CharField(max_length=50, default="Task")  # Epic, Feature, Component, etc.
    color = models.CharField(max_length=20)  # green, yellow, orange, etc.
    
    # Position data for canvas view
    pos_x = models.FloatField()  # Position as percentage of canvas width
    pos_y = models.FloatField()  # Position as percentage of canvas height
    
    # Simple priority and size
    priority = models.CharField(max_length=20, default="Medium")  # Critical, High, Medium, Low
    size = models.CharField(max_length=10, default="M")  # 1, 2, 3, 5, 8, 13 or S, M, L, XL
    
    # Acceptance criteria
    acceptance_criteria = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Blocked status details
    blocked = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title



class PostNoteLink(models.Model):
    """Model for storing links between post notes"""
    source = models.ForeignKey(PostNote, on_delete=models.CASCADE, related_name='outgoing_links')
    target = models.ForeignKey(PostNote, on_delete=models.CASCADE, related_name='incoming_links')
    link_type = models.CharField(max_length=50)  # 'depends_on', 'related_to', 'parent_of', etc.
    
    # Connection point positions - with null=True to fix migration issues
    SOURCE_POSITIONS = [
        ('left', 'Left'),
        ('right', 'Right'),
        ('top', 'Top'),
        ('bottom', 'Bottom'),
    ]
    
    TARGET_POSITIONS = [
        ('left', 'Left'),
        ('right', 'Right'),
        ('top', 'Top'),
        ('bottom', 'Bottom'),
    ]
    
    source_position = models.CharField(max_length=10, choices=SOURCE_POSITIONS, default='right', null=True, blank=True)
    target_position = models.CharField(max_length=10, choices=TARGET_POSITIONS, default='left', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('source', 'target', 'link_type')
    
    def __str__(self):
        return f"{self.source.title} {self.link_type} {self.target.title}"
    

# class PostNoteLink(models.Model):
#     """Model for storing links between post notes"""
#     source = models.ForeignKey(PostNote, on_delete=models.CASCADE, related_name='outgoing_links')
#     target = models.ForeignKey(PostNote, on_delete=models.CASCADE, related_name='incoming_links')
#     link_type = models.CharField(max_length=50)  # 'depends_on', 'related_to', 'parent_of', etc.
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         unique_together = ('source', 'target', 'link_type')
    
#     def __str__(self):
#         return f"{self.source.title} {self.link_type} {self.target.title}"

