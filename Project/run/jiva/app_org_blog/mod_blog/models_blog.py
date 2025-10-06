
from app_org_blog.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_member.models_member import Member
from django.utils import timezone
from markdownx.models import MarkdownxField

class Blog(BaseModelImpl):
    organization = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="organization_app_blogs", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="app_author_blogs")
    
    # Enhanced blog fields
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    content = MarkdownxField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    
    # Status and categorization
    status = models.CharField(max_length=20, 
                           choices=[('draft', 'Draft'), 
                                   ('published', 'Published'),
                                   ('archived', 'Archived')],
                           default='draft')
    category = models.CharField(max_length=50, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)  # Comma-separated tags
    
    # Publishing details
    published_at = models.DateTimeField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Auto-set title from name if not provided
        if not self.title and self.name:
            self.title = self.name
            
        # Auto-set published date when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)
   
    def __str__(self):
        if self.title:
            return self.title
        elif self.name:
            return self.name
        else:
            return str(self.id)
            
class BlogComment(BaseModelImpl):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="blog_comments")
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="replies")
    
    def __str__(self):
        return f"Comment by {self.author.username if self.author else 'Anonymous'} on {self.blog.title if self.blog and self.blog.title else 'unknown blog'}"

# Define blog-specific roles
class BlogMember(BaseModelImpl):
    ROLE_CHOICES = [
        ('admin', 'Blog Admin'),
        ('writer', 'Writer'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_members")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="blog_roles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    
    class Meta:
        unique_together = ('blog', 'member')
        
    def __str__(self):
        return f"{self.member.user.username if self.member and self.member.user else 'Unknown'} - {self.get_role_display()} for {self.blog.title if self.blog and self.blog.title else 'Unknown blog'}"
