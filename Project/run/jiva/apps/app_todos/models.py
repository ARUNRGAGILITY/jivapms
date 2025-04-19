from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.conf import settings

# Using the BaseModel and TreeBaseModel from your provided code
class BaseModel(models.Model):
    """
    Base model for all models that need CRUD functionality
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # New fields
    blocked = models.BooleanField(default=False)
    blocked_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ['position']
    
    def soft_delete(self):
        """Soft deletes the object by setting active=False"""
        self.active = False
        self.save()
    
    def restore(self):
        """Restores a soft-deleted object by setting active=True"""
        self.active = True
        self.save()
    
    def permanent_delete(self):
        """Marks the object for permanent deletion by setting deleted=True and active=False"""
        self.active = False
        self.deleted = True
        self.save()
        
    def mark_done(self):
        """Marks the object as done and sets the done timestamp"""
        self.done = True
        self.done_at = timezone.now()
        self.save()
        
    def block(self):
        """Blocks the object and sets the blocked timestamp"""
        self.blocked = True
        self.blocked_at = timezone.now()
        self.save()
        
    def unblock(self):
        """Unblocks the object"""
        self.blocked = False
        self.blocked_at = None
        self.save()


class TreeBaseModel(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    class MPTTMeta:
        order_insertion_by = ['position']

    class Meta:
        abstract = True

    def active_children(self):
        return self.get_children().filter(active=True, deleted=False)

    def deleted_children(self):
        return self.get_children().filter(deleted=True)

    def subtree_progress(self):
        """Calculate progress of self + children: (done / total) * 100"""
        subtree_nodes = self.get_descendants(include_self=True).filter(active=True, deleted=False)
        total = subtree_nodes.count()
        if total == 0:
            return 0
        done_count = subtree_nodes.filter(done=True).count()
        return round((done_count / total) * 100, 2)

    def copy_node(self, parent=None):
        """
        Shallow copy the current node (no children) to the given parent.
        """
        new_node = self.__class__.objects.get(pk=self.pk)
        new_node.pk = None
        new_node.parent = parent
        new_node.name = f"{self.name} (copy)"
        new_node.created_at = timezone.now()
        new_node.updated_at = timezone.now()
        new_node.done = False
        new_node.done_at = None
        new_node.blocked = False
        new_node.blocked_at = None
        new_node.save()
        return new_node

    def deep_copy(self, parent=None):
        """
        Deep copy the current node and all its children recursively.
        """
        new_node = self.copy_node(parent=parent)
        for child in self.get_children():
            child.deep_copy(parent=new_node)
        return new_node


class Todo(TreeBaseModel):
    """Todo model that extends TreeBaseModel for hierarchical todo lists"""
    # Additional fields for Todo
    start_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    
    PRIORITY_CHOICES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    # Foreign keys
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    kanban_column = models.ForeignKey('KanbanColumn', null=True, blank=True, on_delete=models.SET_NULL, related_name='kc_todos')
    my_todos = models.ForeignKey('MyTodos', null=True, blank=True, on_delete=models.SET_NULL, related_name='mtd_todos')
    
    # Add owner field to link with User model
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', null=True, blank=True)
    # For Canvas View - storing position
    canvas_x = models.IntegerField(default=0)
    canvas_y = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
    
    def __str__(self):
        return self.name


class KanbanColumn(BaseModel):
    """Model for Kanban columns"""
    wip_limit = models.IntegerField(default=0)  # 0 means no limit
    is_default = models.BooleanField(default=False)
    column_type = models.CharField(max_length=20, default='custom', 
                                 choices=(('todo', 'Todo'), ('done', 'Done'), ('custom', 'Custom')))
    my_todos = models.ForeignKey('app_todos.MyTodos', on_delete=models.CASCADE, related_name='kanban_columns', null=True, blank=True)
    class Meta:
        verbose_name = "Kanban Column"
        verbose_name_plural = "Kanban Columns"
    
    def __str__(self):
        return self.name
    
    def todo_count(self):
        return Todo.objects.filter(
            active=True, 
            deleted=False, 
            kanban_column=self
        ).count()


# MyTodos model - parent container for different todo lists
class MyTodos(BaseModel):
    """Model for categorizing todos into different lists (Office, Personal, etc.)"""
    icon = models.CharField(max_length=50, default="fa-list")  # FontAwesome icon
    color = models.CharField(max_length=20, default="primary")  # Bootstrap color class
     # Add owner field to link with User model
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_lists', null=True, blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Todo List"
        verbose_name_plural = "Todo Lists"
        ordering = ['position']
    
    def __str__(self):
        return self.name
    
    def todo_count(self):
        """Return count of active todos in this list"""
        return Todo.objects.filter(
            active=True,
            deleted=False,
            my_todos=self
        ).count()
    
    def done_count(self):
        """Return count of completed todos in this list"""
        return Todo.objects.filter(
            active=True,
            deleted=False,
            my_todos=self,
            done=True
        ).count()
    
    def soft_delete(self):
        """Mark as deleted instead of actually deleting"""
        self.deleted = True
        self.active = False
        self.save()
        
    def restore(self):
        """Restore from trash"""
        self.deleted = False
        self.active = True
        self.save()

    def is_shared_with(self, user):
        return self.shares.filter(shared_with=user).exists()
    
    def can_user_edit(self, user):
        if user == self.owner:
            return True
        return self.shares.filter(shared_with=user, can_edit=True).exists()


class TodoShare(models.Model):
    """Model to handle sharing of todo lists"""
    todo_list = models.ForeignKey('MyTodos', on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_todos')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_shares')
    can_edit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('todo_list', 'shared_with')
        verbose_name = 'Todo List Share'
        verbose_name_plural = 'Todo List Shares'
    
    def __str__(self):
        return f"{self.todo_list.name} shared with {self.shared_with.username} by {self.shared_by.username}"
    

class AccountProfile(models.Model):
    """Model to handle user profiles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username