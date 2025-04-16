from django.db import models

# Create your models here.
class CommonBaseModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
    # position for sequence
    position = models.PositiveIntegerField(default=1000)
    
    # date details
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # active or deleted
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    
    # blocked
    blocked = models.BooleanField(default=False)
    blocked_count = models.PositiveIntegerField(default=0)
    
    # done and at time
    done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)
    
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['position']
        abstract = True
    
    def __str__(self):
        return self.name